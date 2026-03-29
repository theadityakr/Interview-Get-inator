from worker.portal_worker import run_portal_task

class PortalService:
    _stop_flag = False

    @staticmethod
    def stop():
        PortalService._stop_flag = True

    @staticmethod
    async def apply_portal(url: str, max_jobs: int, max_minutes: int):
        PortalService._stop_flag = False
        return await run_portal_task(url, max_jobs, max_minutes, PortalService)