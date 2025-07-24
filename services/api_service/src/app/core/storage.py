from minio import Minio
from fastapi import UploadFile
import os
import uuid

from pydantic import HttpUrl

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "images")

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Ensure bucket exists
if not client.bucket_exists(MINIO_BUCKET):
    client.make_bucket(MINIO_BUCKET)

async def upload_to_object_store(file: UploadFile) -> HttpUrl:
    object_name = f"{uuid.uuid4()}-{file.filename}"
    content = await file.read()

    client.put_object(
        bucket_name=MINIO_BUCKET,
        object_name=object_name,
        data=content,
        length=len(content),
        content_type=file.content_type
    )

    return HttpUrl(f"http://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{object_name}")
