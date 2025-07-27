import asyncio
import os
from typing import Any

from fastapi import UploadFile
from minio import Minio
from qdrant_client.http.models import VectorParams, Distance
from sqlalchemy.ext.asyncio import AsyncEngine

from dependencies.celery import get_celery_client
from dependencies.object_store import get_object_store_client
from dependencies.vector_db import get_vector_db_client
from shared.config.object_store import ObjectStoreSettings
from shared.config.vector_db import VectorDBSettings
from shared.custom_types.enums import DistanceMetric
from shared.models.base import Base

DISTANCE_MAP = {
    DistanceMetric.COSINE: Distance.COSINE,
    DistanceMetric.EUCLID: Distance.EUCLID,
    DistanceMetric.DOT: Distance.DOT,
}


async def upload_file_to_minio(minio_client: Minio, file: UploadFile, bucket_name: str, object_key: str) -> None:
    """Uploads a file to MinIO using threading to avoid blocking the event loop.

    Args:
        minio_client (Minio): MinIO client instance.
        file (UploadFile): The uploaded file from FastAPI.
        bucket_name (str): Target bucket in MinIO.
        object_key (str): Target object key (path/name) in MinIO.

    Returns:
        int: Size of the uploaded file in bytes.
    """
    file_obj = file.file

    file_obj.seek(0, os.SEEK_END)
    size = file_obj.tell()
    file_obj.seek(0)

    await asyncio.to_thread(
        minio_client.put_object,
        bucket_name,
        object_key,
        file_obj,
        size,
        content_type=file.content_type
    )


async def send_celery_task_async(task_name: str, *args: Any) -> None:
    client = get_celery_client()
    loop = asyncio.get_running_loop()

    await loop.run_in_executor(
        None,
        lambda: client.send_task(task_name, args=args)
    )


async def init_minio_bucket(object_store_config: ObjectStoreSettings):
    """Do not use it in prod later. Let CI handle this outside the app."""
    try:
        print(f"MinIO bucket name: {object_store_config.bucket}")
        minio = get_object_store_client()
        if not minio.bucket_exists(object_store_config.bucket):
            minio.make_bucket(object_store_config.bucket)
            print(f"Created bucket: {object_store_config.bucket}")
    except Exception as e:
        print(e)
        raise RuntimeError


async def init_vector_db_collection(vector_db_config: VectorDBSettings):
    try:
        qdrant = await get_vector_db_client()
        if not await qdrant.collection_exists(vector_db_config.collection):
            distance = DISTANCE_MAP[vector_db_config.distance_metric]
            await qdrant.create_collection(
                collection_name=vector_db_config.collection,
                vectors_config=VectorParams(size=vector_db_config.vector_size, distance=distance)
            )
            print(f"Created Qdrant collection: {vector_db_config.collection}")
    except Exception as e:
        print(e)
        raise RuntimeError


async def create_schema(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
