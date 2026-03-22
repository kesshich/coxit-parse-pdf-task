from fastapi import APIRouter

from backend.db.mongo.repositories.repository import get_all_history
from backend.schemas.history import HistoryRecord

router = APIRouter(prefix="/history")


@router.get("/", response_model=list[HistoryRecord])
async def list_history():
    return await get_all_history()
