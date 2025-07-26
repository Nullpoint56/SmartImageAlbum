from datetime import datetime, UTC
import uuid
from types import SimpleNamespace
from typing import Optional

from worker.config import WorkerConfig
from worker.executors import STEP_EXECUTORS
from worker.dependencies import get_session, get_minio_client, get_embedder_client, get_qdrant_client
from shared.models import ImageProcessingJob
from shared.custom_types.enums import JobStatus
from worker.app import celery_app


@celery_app.task(name="process_image")
def process_image(image_id: uuid.UUID):
    config = WorkerConfig()

    db = get_session(config)
    job: Optional[ImageProcessingJob] = db.get(ImageProcessingJob, image_id)

    if not job:
        raise RuntimeError(f"No job found for image_id={image_id}")

    job.status = JobStatus.PROCESSING
    db.commit()

    deps = SimpleNamespace(
        config=config,
        db=db,
        minio=get_minio_client(config),
        embedder=get_embedder_client(config),
        qdrant=get_qdrant_client(config),
    )

    for step in sorted(job.steps, key=lambda s: s.step_index):
        if step.done:
            continue

        try:
            step.started_at = datetime.now(UTC)
            fn = STEP_EXECUTORS[step.step_name]
            fn(job=job, step=step, deps=deps)
            step.done = True
            step.finished_at = datetime.now(UTC)
            db.commit()

        except Exception as e:
            step.error = str(e)
            job.status = JobStatus.ERROR
            db.commit()
            raise

    if job.is_completed:
        job.status = JobStatus.DONE
        db.commit()
