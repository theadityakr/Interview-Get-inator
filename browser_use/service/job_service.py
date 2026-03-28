from fastapi import BackgroundTasks
from worker.agent_worker import run_agent_task


class JobService:

    @staticmethod
    def apply_job_async(url: str, background_tasks: BackgroundTasks):
        background_tasks.add_task(run_agent_task, url)