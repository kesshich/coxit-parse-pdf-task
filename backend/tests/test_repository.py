from datetime import datetime, timezone

from bson import ObjectId

from backend.db.mongo.repositories.repository import _to_record
from backend.schemas.history import HistoryRecord


def _make_doc(result: str = "summary text", filename: str = "test.pdf") -> dict:
    return {
        "_id": ObjectId(),
        "filename": filename,
        "result": result,
        "created_at": datetime.now(timezone.utc),
    }


def test_to_record_returns_history_record():
    doc = _make_doc()
    record = _to_record(doc)
    assert isinstance(record, HistoryRecord)


def test_to_record_maps_id():
    doc = _make_doc()
    record = _to_record(doc)
    assert record.id == str(doc["_id"])


def test_to_record_maps_all_fields():
    doc = _make_doc(result="my summary", filename="report.pdf")
    record = _to_record(doc)
    assert record.filename == "report.pdf"
    assert record.result == "my summary"
    assert record.created_at == doc["created_at"]

