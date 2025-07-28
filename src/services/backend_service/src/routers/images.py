import uuid
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from minio import Minio
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, ScoredPoint
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from config.app import AppConfig, get_app_config
from dependencies.db import get_db_session
from dependencies.object_store import get_object_store_client
from dependencies.vector_db import get_vector_db_client
from schemas.images import ScoredImageSchema, ImageSchema, ImageFeaturesSchema, ImageMetadataSchema
from shared.models import Image
from shared.models.image import ImageMetadata
from utils import send_celery_task_async, upload_file_to_minio

image_router = APIRouter(prefix="/images", tags=["images"])


@image_router.post("/upload", response_model=dict)
async def upload_image(
        file: Annotated[UploadFile, File(...)],
        db: Annotated[AsyncSession, Depends(get_db_session)],
        minio_client: Annotated[Minio, Depends(get_object_store_client)],
        config: Annotated[AppConfig, Depends(get_app_config)]
):
    image_id = uuid.uuid4()
    ext = file.filename.split(".")[-1]
    object_key = f"{config.object_store.bucket}/{image_id}.{ext}"

    try:
        await upload_file_to_minio(minio_client, file, config.object_store.bucket, object_key)

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

        await send_celery_task_async("process_image", str(image_id))

        return {"id": str(image_id)}
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {e}",
        )


@image_router.get("/{image_id}", response_model=ImageSchema)
async def get_image(
        image_id: uuid.UUID,
        db: Annotated[AsyncSession, Depends(get_db_session)],
        qdrant: Annotated[AsyncQdrantClient, Depends(get_vector_db_client)],
        config: Annotated[AppConfig, Depends(get_app_config)]
):
    # 1. Load metadata from DB
    result = await db.execute(
        select(ImageMetadata).join(Image).where(Image.id == image_id)
    )
    metadata = result.scalar_one_or_none()

    if not metadata:
        raise HTTPException(status_code=404, detail="Image metadata not found")

    # 2. Load vector from Qdrant

    qdrant_response = await qdrant.query_points(
        collection_name=config.vector_db.collection,
        query_filter=Filter(
            must=[FieldCondition(key="image_id", match=MatchValue(value=str(image_id)))]
        ),
        limit=1,
        with_vectors=True,
        with_payload=True
    )

    points = qdrant_response.points
    if not points or points[0].vector is None:
        raise HTTPException(status_code=404, detail="Image not found or missing vector")

    vector = points[0].vector
    features = ImageFeaturesSchema(
        vector=vector,
        dimension=len(vector)
    )

    # 3. Assemble response
    return ImageSchema(
        id=image_id,
        metadata=ImageMetadataSchema(
            filename=metadata.filename,
            content_type=metadata.content_type,
            size_bytes=metadata.size_bytes,
            embedding_model=metadata.embedding_model
        ),
        features=features
    )


@image_router.get("/{image_id}/similar", response_model=list[ScoredImageSchema])
async def get_similar_images(
    image_id: uuid.UUID,
    qdrant: Annotated[AsyncQdrantClient, Depends(get_vector_db_client)],
    config: Annotated[AppConfig, Depends(get_app_config)],
):
    # 1. Fetch original image vector using payload filter
    scroll_result = await qdrant.scroll(
        collection_name=config.vector_db.collection,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="image_id",
                    match=MatchValue(value=str(image_id))
                )
            ]
        ),
        limit=1,
        with_vectors=True,
        with_payload=True,
    )

    if not scroll_result or not scroll_result[0]:
        raise HTTPException(status_code=404, detail="Image not found")

    point = scroll_result[0][0]
    query_vector = point.vector
    if query_vector is None:
        raise HTTPException(status_code=404, detail="Vector not found for image")

    # 2. Use query_points for similarity search (replacement for search)
    response = await qdrant.query_points(
        collection_name=config.vector_db.collection,
        query=query_vector,
        limit=config.vector_db.top_k + 1,
        with_vectors=False,
        with_payload=True,
    )

    results: list[ScoredImageSchema] = []
    for point in response.points:
        payload = point.payload or {}
        raw_image_id = payload.get("image_id")
        if not raw_image_id or str(raw_image_id) == str(image_id):
            continue
        results.append(ScoredImageSchema(
            id=uuid.UUID(str(raw_image_id)),
            score=point.score,
        ))
        if len(results) >= config.vector_db.top_k:
            break

    return results
