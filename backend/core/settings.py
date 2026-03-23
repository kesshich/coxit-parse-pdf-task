from backend.core.config import SettingsABC


class AppSettings(SettingsABC):
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

