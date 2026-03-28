from browser_use import Agent
from .env import get_env
from .llm_config import LLMConfig
from .browser_config import BrowserFactory
from tools.custom_tools import tools


DEFAULT_TASK = """
Autonomous job application agent:
- detect job pages
- fill forms using resume
- avoid duplicates
- stop on captcha
"""


class AgentFactory:

    @staticmethod
    def create(
        task_override: str = None,
        resume_path: str = None
    ):
        return Agent(
            # ✅ Task override support
            task=task_override if task_override else DEFAULT_TASK,

            # ===== LLM =====
            llm=LLMConfig.primary(),
            fallback_llm=LLMConfig.fallback(),
            page_extraction_llm=LLMConfig.extraction(),

            # ===== Browser =====
            browser=BrowserFactory.create(),

            # ===== Tools =====
            tools=tools,

            # ===== Behavior =====
            use_vision=get_env("USE_VISION", "true") == "true",
            vision_detail_level=get_env("VISION_DETAIL", "high"),

            max_actions_per_step=int(get_env("MAX_ACTIONS_PER_STEP", 5)),
            max_failures=int(get_env("MAX_FAILURES", 5)),

            # ===== Files =====
            save_conversation_path=get_env("LOG_PATH"),
            available_file_paths=[resume_path] if resume_path else [
                get_env("RESUME_PATH")
            ],

            # ===== Debug =====
            generate_gif="logs/agent.gif" if get_env("GENERATE_GIF") == "true" else "false"
        )