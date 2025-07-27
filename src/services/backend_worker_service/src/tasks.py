import uuid
from datetime import datetime, UTC

from shared.custom_types.enums import JobStatus
from shared.models.jobs import ImageProcessingJob, JobStep
from shared.custom_types.enums import JobStepName

from app import celery_app
from dependencies import WorkerContext
from executors import STEP_EXECUTORS
from config import WorkerConfig


@celery_app.task(name="process_image", autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def process_image(image_id: uuid.UUID):
    steps_to_run = [JobStepName.EMBEDDING, JobStepName.INDEXING]
    config = WorkerConfig()
    ctx = WorkerContext(config)

    # Create job record
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

    # Shared execution state
    state = {}

    for step in sorted(job.steps, key=lambda s: s.step_index):
        if step.done:
            continue

        try:
            step.started_at = datetime.now(UTC)
            fn = STEP_EXECUTORS[step.step_name]
            fn(job=job, step=step, ctx=ctx, state=state)
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
