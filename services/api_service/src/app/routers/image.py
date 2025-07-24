import mimetypes
from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.coordinator import notify_coordinator
from app.core.storage import upload_to_object_store
from app.dependencies import get_db
from app.models.image import Image
from app.schemas.image import ImageUploadResponse, ImageMetadataResponse, SimilarImageResponse

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):
    # 1. Upload to object store
    object_url = await upload_to_object_store(file)

    # 2. Store metadata in DB
    image = Image(
        filename=file.filename,
        content_type=file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream",
        url=object_url
    )
    db.add(image)
    await db.commit()
    await db.refresh(image)

    # 3. Notify coordinator in background
    background_tasks.add_task(notify_coordinator, image.id)

    return ImageUploadResponse(image_id=image.id, url=object_url)


@router.get("/{image_id}", response_model=ImageMetadataResponse)
async def get_image_metadata(image_id: UUID, db: AsyncSession = Depends(get_db)):
    image = await db.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return ImageMetadataResponse(
        image_id=image.id,
        filename=image.filename,
        content_type=image.content_type,
        url=image.url,
        embedding=eval(image.embedding) if image.embedding else None
    )


@router.get("/{image_id}/similar", response_model=SimilarImageResponse)
async def get_similar_images(image_id: UUID) -> SimilarImageResponse:
    # TODO: Call vector DB
    return SimilarImageResponse(matches=[])
