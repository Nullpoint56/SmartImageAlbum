from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from PIL import Image
from io import BytesIO
import torch
from transformers import CLIPProcessor, CLIPModel

from image_embedding_service.dependencies import get_model_and_processor

embed_router = APIRouter(prefix="", tags=["embedding"])


@embed_router.post("/encode")
async def encode_image(

    deps: tuple[CLIPModel, CLIPProcessor, torch.device] = Depends(get_model_and_processor),
) -> JSONResponse:
    """
    Accept an image and return the embedding vector.

    Args:
        file (UploadFile): The uploaded image.
        deps (tuple): Injected (model, processor, device)

    Returns:
        JSONResponse: Embedding as list of floats.
    """
    model, processor, device = deps

    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid image format")

    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        features = model.get_image_features(**inputs)
        normalized = features[0] / features[0].norm()

    return JSONResponse(content={"embedding": normalized.cpu().tolist()})
