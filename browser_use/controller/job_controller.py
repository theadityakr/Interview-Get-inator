from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.job_service import JobService

class JobRequest(BaseModel):
    url: str

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs"])

@router.post("/apply")
async def apply_job(request: JobRequest):
    try:
        await JobService.apply_job(request.url)
        return {
            "status": "completed",
            "message": "Job application finished"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))