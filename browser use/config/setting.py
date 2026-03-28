from .agent_config import AgentFactory

class Settings:

    @staticmethod
    def get_agent():
        return AgentFactory.create()