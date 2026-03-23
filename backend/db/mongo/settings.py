from pydantic import MongoDsn

from backend.core.config import SettingsABC


class MongoSettings(SettingsABC):
    MONGO_URI: MongoDsn
    MONGO_DB: str
    HISTORY_LIMIT: int = 5


settings = MongoSettings()

