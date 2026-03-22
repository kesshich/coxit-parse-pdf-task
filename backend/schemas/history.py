from datetime import datetime

from pydantic import BaseModel


class HistoryRecord(BaseModel):
    id: str
    filename: str
    result: str
    created_at: datetime

