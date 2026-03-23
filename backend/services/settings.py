from backend.core.config import SettingsABC


class PDFSettings(SettingsABC):
    # PDF limits
    MAX_FILE_SIZE_MB: int = 50
    MAX_PAGES: int = 100

    # Chunking
    CHUNK_SIZE: int = 2000   # characters per chunk
    CHUNK_OVERLAP: int = 200  # overlap between consecutive chunks

    # "fast"   — pdfminer only, no system deps (local dev / Windows)
    # "hi_res" — OCR + table detection, requires Poppler & Tesseract (Docker)
    PDF_STRATEGY: str = "fast"


settings = PDFSettings()

