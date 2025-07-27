from io import BytesIO
from typing import cast

from PIL import Image
from fastapi import APIRouter, HTTPException, Request
from starlette.concurrency import run_in_threadpool

from ai.model_management import CLIPEmbeddingService
from shared.custom_types.schemas import EmbeddingRequest, EmbeddingResponse
from utils import get_image_bytes

embed_router = APIRouter(prefix="", tags=["embedding"])


@embed_router.post("/encode")
async def encode_image(request: Request, payload: EmbeddingRequest) -> EmbeddingResponse:
    # TODO: Add caching by image_id and model_id
    try:
        image_bytes = await get_image_bytes(str(payload.url))

        def blocking_pipeline() -> EmbeddingRequest:
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
            model_service = cast(CLIPEmbeddingService, request.state.model_service)
            embedding = model_service.encode(image)
            return EmbeddingResponse(
                image_id=payload.image_id,
                model_name=model_service.model_id,
                embedding=embedding,
                dimension=len(embedding)
            )

        return await run_in_threadpool(blocking_pipeline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

