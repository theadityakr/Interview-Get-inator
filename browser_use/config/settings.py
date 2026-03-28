from config.env import get_env
from config.agent_config import AgentFactory


class Settings:

    @staticmethod
    def get_agent():
        return AgentFactory.create()

    @staticmethod
    def get_resume_path():
        return get_env("RESUME_PATH")