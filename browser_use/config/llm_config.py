from browser_use import ChatOpenAI, ChatBrowserUse, ChatGoogle, ChatAnthropic
# from langchain_openai import AzureChatOpenAI
from .env import get_env


def build_llm(model_key: str):
    provider = get_env("LLM_PROVIDER", "openai").lower()
    model = get_env(model_key)

    if provider == "browseruse":
        return ChatBrowserUse()

    if provider == "google":
        return ChatGoogle(model=model or "gemini-flash-latest")

    if provider == "anthropic":
        return ChatAnthropic(model=model or 'claude-sonnet-4-0', temperature= float(get_env("TEMPERATURE") or 0.0))

    # if provider == "azure":
    #     return AzureChatOpenAI(
    #         azure_deployment=model,
    #         azure_endpoint=get_env("AZURE_OPENAI_ENDPOINT"),
    #         api_key=get_env("AZURE_OPENAI_API_KEY"),
    #         api_version=get_env("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    #     )

    # default: openai
    return ChatOpenAI(model=model)


class LLMConfig:

    @staticmethod
    def primary():
        return build_llm("LLM_MODEL")

    @staticmethod
    def fallback():
        return build_llm("FALLBACK_MODEL")

    @staticmethod
    def extraction():
        return build_llm("EXTRACTION_MODEL")
