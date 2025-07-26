import asyncio
import os
from typing import Any

from fastapi import UploadFile
from minio import Minio

from backend_service.dependencies.celery import get_celery_client


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

async def send_celery_task_async(task_name: str, args: tuple[Any, ...]) -> None:
    client = get_celery_client()
    loop = asyncio.get_running_loop()

    await loop.run_in_executor(
        None,
        lambda: client.send_task(task_name, args=args)
    )