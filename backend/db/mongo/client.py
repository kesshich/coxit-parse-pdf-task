from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from backend.db.mongo.settings import settings

_client = AsyncMongoClient(str(settings.MONGO_URI))

def get_db() -> AsyncDatabase:
    return _client[settings.MONGO_DB]
