from enum import StrEnum

from backend.llm.settings import LLMSettings


class LLMType(StrEnum):
    CHATGPT = "chatgpt"


class LLMFactory:
    settings = LLMSettings()

    @classmethod
    def create(cls):
        match cls.settings.LLM_PROVIDER:
            case LLMType.CHATGPT:
                from langchain_openai import ChatOpenAI

                return ChatOpenAI(
                    api_key=cls.settings.OPENAI_API_KEY,
                    model=cls.settings.GENERATION_MODEL,
                    max_tokens=cls.settings.MAX_TOKENS,
                )
            case _:
                raise ValueError(f"Unsupported LLM provider: {cls.settings.LLM_PROVIDER}")


