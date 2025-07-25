import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from schemas.images import SimilarImageResult, ImageMetadata
from services.db import get_image_by_id
from services.image_upload import handle_image_upload
from services.vector_db import find_similar_images

router = APIRouter()


@router.post("/upload", response_model=ImageMetadata)
async def upload_image(file: UploadFile = File(...), session: AsyncSession = Depends(get_db)):
    return await handle_image_upload(file, session)


@router.get("/{image_id}", response_model=ImageMetadata)
async def get_image_metadata(image_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    """Returns metadata and processing status for an image."""
    metadata = await get_image_by_id(session, image_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Image not found")
    return metadata


@router.get("/{image_id}/similar", response_model=list[SimilarImageResult])
async def similar_images(image_id: uuid.UUID):
    """Performs vector search to find visually similar images."""
    return await find_similar_images(image_id)
