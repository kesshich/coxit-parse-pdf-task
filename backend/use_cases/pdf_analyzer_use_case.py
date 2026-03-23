import asyncio

from backend.db.mongo.repositories.repository import save_history
from backend.llm.llm_service import analyze_chunks
from backend.schemas.pdf import AnalyzeResponse
from backend.services.pdf_service import load_and_split


class PdfAnalyzerUseCase:

    def __init__(self, original_filename: str, tmp_file_path: str):
        self.original_filename = original_filename
        self.tmp_file_path = tmp_file_path

    async def generate_pdf_summary(self) -> AnalyzeResponse:
        # load_and_split is CPU-bound (Unstructured PDF parsing) — run in a thread
        # so the event loop stays free for other requests during processing
        chunks = await asyncio.to_thread(load_and_split, self.tmp_file_path)
        summary = await analyze_chunks(chunks)
        record_id = await save_history(result=summary, filename=self.original_filename)

        return AnalyzeResponse(
            id=record_id,
            filename=self.original_filename,
            result=summary,
        )