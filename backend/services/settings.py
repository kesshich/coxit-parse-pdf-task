from backend.core.config import SettingsABC


class PDFSettings(SettingsABC):
    # PDF limits
    MAX_FILE_SIZE_MB: int = 50
    MAX_PAGES: int = 100

    # Chunking
    CHUNK_SIZE: int = 2000   # characters per chunk
    CHUNK_OVERLAP: int = 200  # overlap between consecutive chunks

    # Unstructured PDF parsing strategy:
    # "auto"   — Unstructured decides per-page (OCR when needed, fast otherwise) [recommended]
    # "fast"   — direct text extraction only, no OCR
    # "hi_res" — full OCR + table detection, requires Poppler & Tesseract
    PDF_STRATEGY: str = "auto"


settings = PDFSettings()

