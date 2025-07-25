import hashlib

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import arq_redis
from schemas.images import ImageMetadata
from services import db
from services.db import enqueue_job


async def handle_image_upload(file: UploadFile, session: AsyncSession) -> ImageMetadata:
    image_bytes = await file.read()
    content_hash = hashlib.sha256(image_bytes).hexdigest()

    existing = await db.get_image_by_hash(session, content_hash)
    if existing:
        return ImageMetadata.model_validate(existing)

    url = await db.store_image_to_object_store(file.filename, image_bytes)

    image = await db.create_image_record(session, filename=file.filename,
                                         content_type=file.content_type,
                                         url=url,
                                         content_hash=content_hash)

    await db.create_job_record(session, image.id)

    await enqueue_job(arq_redis, image.id)

    return ImageMetadata.model_validate(image)
