import os
import tempfile

from fastapi import File, HTTPException, UploadFile

from backend.services.settings import settings
from backend.use_cases.pdf_analyzer_use_case import PdfAnalyzerUseCase


def create_pdf_analyze(file: UploadFile = File(...)):
    size_mb = file.size / (1024 * 1024)
    if size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File size ({size_mb:.1f} MB) exceeds the {settings.MAX_FILE_SIZE_MB} MB limit.",
        )

    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(file.file.read())
        tmp.flush()
    try:
        yield PdfAnalyzerUseCase(original_filename=file.filename, tmp_file_path=tmp.name)
    finally:
        os.unlink(tmp.name)  # always delete the temp file