from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from app.core.orchestrator import run_job_fsm
from app.dependencies import get_db
from app.models.job import Job
from app.schemas.job import JobStatusResponse, JobCreateRequest, JobCreateResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("", response_model=JobCreateResponse, status_code=status.HTTP_201_CREATED)
async def submit_job(
    job_req: JobCreateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    job = await Job.create(db, image_url=str(job_req.image_url))
    background_tasks.add_task(run_job_fsm, job.id)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"id": str(job.id)},
        headers={"Location": f"/jobs/{job.id}/status"}
    )

@router.get("/{job_id}/status", response_model=JobStatusResponse)
async def job_status(job_id: UUID, db: AsyncSession = Depends(get_db)):
    job = await Job.get(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse.model_validate(job)
