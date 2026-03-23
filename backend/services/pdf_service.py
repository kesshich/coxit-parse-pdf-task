import os
import tempfile

from fastapi import HTTPException, UploadFile
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.services.settings import settings


def load_and_split(file: UploadFile) -> list[str]:
    """Load a PDF upload, validate it, and split it into overlapping text chunks.
    Args:
        file: The raw ``UploadFile`` received from the FastAPI route.

    Returns:
        A list of text chunk strings ready to be forwarded to the LLM.

    Raises:
        HTTPException 400: File exceeds the size or page-count limits.
        HTTPException 422: No text content could be extracted from the PDF.
    """
    content = file.file.read()

    # Validate file size
    size_mb = len(content) / (1024 * 1024)
    if size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File size ({size_mb:.1f} MB) exceeds the {settings.MAX_FILE_SIZE_MB} MB limit.",
        )

    # UnstructuredPDFLoader requires a real file path, so write to a temp file
    # and always clean it up afterwards
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        if settings.PDF_STRATEGY == "hi_res":
            loader = UnstructuredPDFLoader(tmp_path, mode="elements", strategy="hi_res")
        else:
            loader = PyPDFLoader(tmp_path)

        docs = loader.load()

        if not docs:
            raise HTTPException(
                status_code=422,
                detail="Could not extract any text from the PDF. "
                       "If the file is scanned or image-based, use the hi_res strategy.",
            )

        # PyPDFLoader uses "page" (0-indexed), UnstructuredPDFLoader uses "page_number" (1-indexed)
        if settings.PDF_STRATEGY == "hi_res":
            max_page = max((doc.metadata.get("page_number") or 0) for doc in docs)
        else:
            max_page = max((doc.metadata.get("page") or 0) for doc in docs) + 1

        if max_page > settings.MAX_PAGES:
            raise HTTPException(
                status_code=400,
                detail=f"PDF exceeds the {settings.MAX_PAGES} page limit.",
            )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )
        return [chunk.page_content for chunk in splitter.split_documents(docs)]

    finally:
        os.unlink(tmp_path)  # always delete the temp file
