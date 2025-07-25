import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from schemas.images import SimilarImageResult, ImageMetadata
from services.image_upload import handle_image_upload

router = APIRouter()

@router.post("/upload", response_model=ImageMetadata)
async def upload_image(file: UploadFile = File(...)):
    """Accepts an image upload and triggers the Coordinator for processing."""
    return await handle_image_upload(file)

@router.get("/{image_id}", response_model=ImageMetadata)
async def get_image_metadata(image_id: uuid.UUID):
    """Returns metadata and processing status for an image."""
    metadata = await get_image_by_id(image_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Image not found")
    return metadata

@router.get("/{image_id}/similar", response_model=list[SimilarImageResult])
async def similar_images(image_id: uuid.UUID):
    """Performs vector search to find visually similar images."""
    return await find_similar_images(image_id)
