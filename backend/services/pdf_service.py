from fastapi import HTTPException
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.services.settings import settings


def load_and_split(tmp_file_path: str) -> list[str]:
    """Load a PDF using Unstructured and split it into overlapping text chunks.

    The strategy is read from settings (default: "auto"). Unstructured's "auto"
    mode decides per-page whether to use direct text extraction or OCR, so both
    plain-text and image-heavy PDFs are handled correctly without any custom logic.

    Args:
        tmp_file_path: Path to the temporary PDF file on disk.

    Returns:
        A list of text chunk strings ready to be forwarded to the LLM.

    Raises:
        HTTPException 400: PDF exceeds the page limit.
        HTTPException 422: No text content could be extracted from the PDF.
    """
    loader = UnstructuredPDFLoader(tmp_file_path, mode="elements", strategy=settings.PDF_STRATEGY)
    docs = loader.load()

    if not docs:
        raise HTTPException(
            status_code=422,
            detail="Could not extract any text from the PDF.",
        )

    # UnstructuredPDFLoader always provides page_number (1-indexed)
    max_page = max((doc.metadata.get("page_number") or 0) for doc in docs)
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