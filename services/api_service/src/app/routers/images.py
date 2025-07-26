import uuid
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from minio import Minio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND

from app.dependencies.db import get_db_session
from app.dependencies.object_store import get_object_store_client
from app.schemas.images import ImageMetadataSchema, ImageFeaturesSchema, ImageSchema, ScoredImageSchema
from app.utils import upload_file_to_minio, send_celery_task_async
from shared.models import ImageProcessingJob
from shared.models.image import Image

router = APIRouter()


@router.post("/images/upload", response_model=dict)
async def upload_image(
        file: Annotated[UploadFile, File(...)],
        db: Annotated[AsyncSession, Depends(get_db_session)],
        minio_client: Annotated[Minio, Depends(get_object_store_client)]
):
    image_id = uuid.uuid4()
    ext = file.filename.split(".")[-1]
    object_key = f"uploads/{image_id}.{ext}"

    try:
        await upload_file_to_minio(minio_client, file, object_key, file.content_type)

        image = Image(
            id=image_id,
            filename=file.filename,
            content_type=file.content_type,
            object_key=object_key,
        )
        db.add(image)
        await db.commit()

        await send_celery_task_async(
            "process_image",
            args=(image_id, object_key)

        )

        return {"id": str(image_id)}
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {e}",
        )


@router.get("/images/{image_id}/similar", response_model=List[ScoredImageSchema])
async def get_similar_images(
    image_id: UUID,
    top_k: int = 5,
    qdrant=Depends(get_vector_db_client),
):
    # 1. Fetch the vector of the original image by ID
    response = await qdrant.retrieve(
        collection_name="images",
        ids=[str(image_id)],
        with_vectors=True,
        with_payload=True
    )

    if not response or len(response) == 0 or response[0].vector is None:
        raise HTTPException(status_code=404, detail="Image not found or missing vector")

    query_vector = response[0].vector

    # 2. Search for similar vectors
    search_result = await qdrant.search(
        collection_name="images",
        query_vector=query_vector,
        limit=top_k + 1,
        with_payload=True
    )

    # 3. Convert to response model, skipping the original image
    results: list[ScoredImageSchema] = []
    for point in search_result:
        if str(point.id) == str(image_id):
            continue
        payload = point.payload or {}

        try:
            metadata = ImageMetadataSchema(
                filename=payload["filename"],
                content_type=payload["content_type"],
                size_bytes=payload["size_bytes"],
            )
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Missing metadata field: {e}")

        results.append(ScoredImageSchema(
            id=UUID(str(point.id)),
            score=point.score,
            metadata=metadata
        ))

        if len(results) >= top_k:
            break

    return results

