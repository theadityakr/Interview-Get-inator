import sys
import asyncio
import uvicorn

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from controller.job_controller import router as job_router
from controller.portal_controller import router as portal_router

app = FastAPI(title="Job Automation API")
app.include_router(job_router)
app.include_router(portal_router)

@app.get("/api/v1/health")
def health():
    return {"status": "running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,  
        loop="asyncio"
    )