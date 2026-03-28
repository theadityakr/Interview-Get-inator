import asyncio
from config.settings import Settings
from config.agent_config import AgentFactory
from config.env import get_env

async def run_agent_task(url: str):
    try:
        resume_path = Settings.get_resume_path()
        task = f"""
        Open the job URL and apply.

        URL: {url}

        IMPORTANT:
        - Use the resume located at {resume_path}
        - Extract candidate details from resume
        - Fill all required fields accurately

        Instructions:
        - Extract job details
        - Fill the application form
        - Submit application
        - Confirm success
        - Stop if captcha appears
        """
        agent = AgentFactory.create(
            task_override=task,
            resume_path=resume_path
        )

        result = await asyncio.wait_for(
            agent.run(int(get_env("MAX_STEPS", 100))),
            timeout=int(get_env("TIME_OUT", 600))
        )

        print(f"Applied successfully: {url}")
        print(result)

    except Exception as e:
        print(f"Failed: {url}")
        print(str(e))