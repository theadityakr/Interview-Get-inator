from fastapi import FastAPI
from controller.job_controller import router as job_router

app = FastAPI(title="Job Automation API")

app.include_router(job_router)


@app.get("/api/v1/health")
def health():
    return {"status": "running"}