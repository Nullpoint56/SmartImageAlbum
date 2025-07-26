import uuid
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from backend_service.dependencies.db import get_db_session
from backend_service.dependencies.object_store import get_object_store_client
from backend_service.dependencies.vector_db import get_vector_db_client
from backend_service.schemas.images import ScoredImageSchema
from backend_service.utils import upload_file_to_minio, send_celery_task_async
from shared.models.image import Image, ImageMetadata

router = APIRouter()


@router.post("/images/upload", response_model=dict)
async def upload_image(
    file: Annotated[UploadFile, File(...)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
    # minio_client: Annotated[Minio, Depends(get_object_store_client)]
):
    image_id = uuid.uuid4()
    ext = file.filename.split(".")[-1]
    object_key = f"uploads/{image_id}.{ext}"

    try:
        print("Image uploaded mock")
        # await upload_file_to_minio(minio_client, file, object_key, file.content_type)

        # Create the Image record
        image = Image(
            id=image_id,
            object_key=object_key,
        )

        # Create the metadata record
        metadata = ImageMetadata(
            image=image,
            filename=file.filename,
            content_type=file.content_type,
            size_bytes=len(await file.read()),
        )

        db.add_all([image, metadata])
        await db.commit()

        await send_celery_task_async("process_image", args=(str(image_id), object_key))

        return {"id": str(image_id)}
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {e}",
        )


@router.get("/images/{image_id}/similar", response_model=list[ScoredImageSchema])
async def get_similar_images(
        image_id: uuid.UUID,
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

        results.append(ScoredImageSchema(
            id=uuid.UUID(str(point.id)),
            score=point.score,
        ))

        if len(results) >= top_k:
            break

    return results
