from typing import Annotated

from fastapi import APIRouter, Depends

from backend.api.dependecies.pdf_analyze import create_pdf_analyze
from backend.schemas.pdf import AnalyzeResponse
from backend.use_cases.pdf_analyzer_use_case import PdfAnalyzerUseCase

router = APIRouter(prefix="/pdf")


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    pdf_analyzer_use_case: Annotated[PdfAnalyzerUseCase, Depends(create_pdf_analyze)],
):
    return await pdf_analyzer_use_case.generate_pdf_summary()
