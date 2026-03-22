import abc
from pydantic_settings import BaseSettings, SettingsConfigDict



class SettingsABC(BaseSettings, abc.ABC):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

