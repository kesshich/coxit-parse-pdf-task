from datetime import datetime, timezone

from backend.db.mongo.client import get_db


async def save_history(filename: str, result: str) -> str:
    doc = {
        "filename": filename,
        "result": result,
        "created_at": datetime.now(timezone.utc),
    }
    inserted = await get_db().history.insert_one(doc)
    return str(inserted.inserted_id)


async def get_latest_summaries() -> list[dict]:
    cursor = get_db().history.find().sort("created_at", -1).limit(5)
    return [_serialize(doc) async for doc in cursor]


def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc

