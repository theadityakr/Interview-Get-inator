from worker.agent_worker import run_agent_task

class JobService:

    @staticmethod
    async def apply_job(url: str):
        await run_agent_task(url)