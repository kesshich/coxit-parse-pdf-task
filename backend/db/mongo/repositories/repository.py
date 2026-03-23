from datetime import datetime, timezone

from backend.db.mongo.client import get_db
from backend.db.mongo.settings import settings
from backend.schemas.history import HistoryRecord


async def save_history(filename: str, summary: str) -> str:
    """Persist a PDF analysis result to the history collection.

    Args:
        filename: Original name of the uploaded PDF file.
        summary: LLM-generated summary text.

    Returns:
        The inserted document's ID as a string.
    """
    doc = {
        "filename": filename,
        "summary": summary,
        "created_at": datetime.now(timezone.utc),
    }
    inserted = await get_db().history.insert_one(doc)
    return str(inserted.inserted_id)


async def get_latest_summaries() -> list[HistoryRecord]:
    """Retrieve the most recent analysis records from the history collection.

    Results are sorted by creation time descending and capped at
    ``settings.HISTORY_LIMIT`` entries.

    Returns:
        A list of validated ``HistoryRecord`` instances.
    """
    cursor = get_db().history.find().sort("created_at", -1).limit(settings.HISTORY_LIMIT)
    return [_to_record(doc) async for doc in cursor]


def _to_record(doc: dict) -> HistoryRecord:
    """Convert a raw MongoDB document to a validated ``HistoryRecord``.
    """
    return HistoryRecord.model_validate({
        "id": str(doc["_id"]),
        "filename": doc["filename"],
        "result": doc["result"],
        "created_at": doc["created_at"],
    })
