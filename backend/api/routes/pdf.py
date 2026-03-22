import asyncio

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.db.mongo.repositories.repository import save_history
from backend.schemas.pdf import AnalyzeResponse
from backend.llm.llm_service import analyze_chunks
from backend.services.pdf_service import load_and_split

router = APIRouter(prefix="/pdf")


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(..., description="PDF file to analyze (max 50 MB, 100 pages)"),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    chunks = await asyncio.to_thread(load_and_split, file)
    result = await analyze_chunks(chunks)

    record_id = await save_history(result=result, filename=file.filename)

    return AnalyzeResponse(
        id=record_id,
        filename=file.filename,
        result=result,
    )
