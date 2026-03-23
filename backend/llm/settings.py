from backend.core.config import SettingsABC


class LLMSettings(SettingsABC):
    LLM_PROVIDER: str = "chatgpt"

    # OpenAI
    OPENAI_API_KEY: str | None = None
    GENERATION_MODEL: str = "gpt-4o"
    MAX_TOKENS: int = 2048


settings = LLMSettings()