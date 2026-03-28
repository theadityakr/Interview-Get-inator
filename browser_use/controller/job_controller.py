from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from service.job_service import JobService

class JobRequest(BaseModel):
    url: str

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs"])

@router.post("/apply")
async def apply_job(request: JobRequest, bg: BackgroundTasks):
    try:
        JobService.apply_job_async(request.url, bg)
        return {
            "status": "accepted",
            "message": "Job application started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))