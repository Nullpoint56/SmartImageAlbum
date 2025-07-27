from datetime import datetime, UTC
import uuid

from app import celery_app
from config import WorkerConfig
from dependencies import WorkerContext
from shared.custom_types.enums import JobStatus, JobStepName
from shared.models.jobs import ImageProcessingJob, JobStep

from steps import run_embed
from steps import run_index


@celery_app.task(name="process_image", autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def process_image(image_id: uuid.UUID):
    # Define steps inline with corresponding logic
    steps_to_run = {
        JobStepName.EMBEDDING: run_embed,
        JobStepName.INDEXING: run_index,
    }

    config = WorkerConfig()
    ctx = WorkerContext(config)

    # Create a new job with configured steps
    job = ImageProcessingJob(
        image_id=image_id,
        status=JobStatus.PROCESSING,
        steps=[
            JobStep(step_name=name, step_index=i)
            for i, name in enumerate(steps_to_run)
        ],
    )
    ctx.db.add(job)
    ctx.db.commit()

    state = {}  # Shared memory between steps

    for step in sorted(job.steps, key=lambda s: s.step_index):
        if step.done:
            continue
        try:
            step.started_at = datetime.now(UTC)
            step_fn = steps_to_run[step.step_name]
            step_fn(job=job, ctx=ctx, state=state)
            step.done = True
            step.finished_at = datetime.now(UTC)
            ctx.db.commit()

        except Exception as e:
            step.error = str(e)
            job.status = JobStatus.ERROR
            ctx.db.commit()
            raise

    if job.is_completed:
        job.status = JobStatus.DONE
        ctx.db.commit()

    ctx.close()
