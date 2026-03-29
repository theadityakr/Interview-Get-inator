from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.portal_service import PortalService

class PortalRequest(BaseModel):
    url: str
    max_jobs: int = 50
    max_minutes: int = 10

router = APIRouter(prefix="/api/v1/portal", tags=["Portal"])

@router.post("/apply")
async def apply_portal(request: PortalRequest):
    try:
        result = await PortalService.apply_portal(
            request.url,
            request.max_jobs,
            request.max_minutes
        )
        return {
            "status": "completed",
            "message": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_portal():
    PortalService.stop()
    return {"status": "stopped", "message": "Portal application stopped"}