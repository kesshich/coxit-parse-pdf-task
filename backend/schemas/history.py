from datetime import datetime

from pydantic import BaseModel


class HistoryRecord(BaseModel):
    id: str
    filename: str
    summary: str
    created_at: datetime

