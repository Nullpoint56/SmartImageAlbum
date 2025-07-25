# app/services/db.py

import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from shared.db_models import Image, ImageProcessingJob, JobStatus

from minio import Minio
import aiofiles

from arq.connections import ArqRedis


minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

BUCKET_NAME = "images"


async def get_image_by_hash(session: AsyncSession, content_hash: str) -> Optional[Image]:
    stmt = select(Image).where(Image.content_hash == content_hash)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_image_by_id(session: AsyncSession, image_id: uuid.UUID) -> Optional[Image]:
    stmt = select(Image).where(Image.id == image_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def store_image_to_object_store(filename: str, content: bytes) -> str:
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)

    object_name = f"{uuid.uuid4()}-{filename}"
    async with aiofiles.tempfile.NamedTemporaryFile(delete=False) as tmp:
        await tmp.write(content)
        tmp_path = tmp.name

    minio_client.fput_object(BUCKET_NAME, object_name, tmp_path)

    return f"http://{settings.MINIO_ENDPOINT}/{BUCKET_NAME}/{object_name}"


async def create_image_record(session: AsyncSession, filename: str, content_type: str,
                              url: str, content_hash: str) -> Image:
    image = Image(
        filename=filename,
        content_type=content_type,
        url=url,
        content_hash=content_hash
    )
    session.add(image)
    await session.commit()
    await session.refresh(image)
    return image


async def create_job_record(session: AsyncSession, image_id: uuid.UUID) -> ImageProcessingJob:
    job = ImageProcessingJob(image_id=image_id, status=JobStatus.CREATED)
    session.add(job)
    await session.commit()
    return job


async def enqueue_job(arq_redis: ArqRedis, image_id: uuid.UUID) -> None:
    await arq_redis.enqueue_job("process_image", image_id=str(image_id))
