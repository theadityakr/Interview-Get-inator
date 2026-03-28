from browser_use import ChatOpenAI
from .env import get_env

class LLMConfig:

    @staticmethod
    def primary():
        return ChatOpenAI(
            model=get_env("LLM_MODEL"),
            temperature=float(get_env("LLM_TEMPERATURE", 0.1)),
            # max_tokens=int(get_env("LLM_MAX_TOKENS", 2000))
        )

    @staticmethod
    def fallback():
        return ChatOpenAI(
            model=get_env("FALLBACK_MODEL"),
            temperature=0.2
        )

    @staticmethod
    def extraction():
        return ChatOpenAI(
            model=get_env("EXTRACTION_MODEL")
        )