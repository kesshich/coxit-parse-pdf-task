import os
import tempfile

from fastapi import HTTPException, UploadFile
from langchain_community.document_loaders import UnstructuredPDFLoader
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
    if size_mb > settings.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File size ({size_mb:.1f} MB) exceeds the {settings.max_file_size_mb} MB limit.",
        )

    # UnstructuredPDFLoader requires a real file path, so write to a temp file
    # and always clean it up afterwards
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # strategy="hi_res" enables OCR for scanned pages and proper table detection
        loader = UnstructuredPDFLoader(tmp_path, mode="elements", strategy="hi_res")
        docs = loader.load()

        if not docs:
            raise HTTPException(
                status_code=422,
                detail="Could not extract any content from the PDF.",
            )

        # Validate page count via element metadata
        max_page = max((doc.metadata.get("page_number") or 0) for doc in docs)
        if max_page > settings.max_pages:
            raise HTTPException(
                status_code=400,
                detail=f"PDF exceeds the {settings.max_pages} page limit.",
            )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        return [chunk.page_content for chunk in splitter.split_documents(docs)]

    finally:
        os.unlink(tmp_path)  # always delete the temp file
