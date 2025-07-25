import uuid
from typing import List

from qdrant_client.grpc import PayloadIncludeSelector
from qdrant_client.models import ScoredPoint
from app.dependencies import qdrant
from schemas.images import SimilarImageResult

VECTOR_COLLECTION = "image_vectors"

async def find_similar_images(image_id: uuid.UUID, top_k: int = 5) -> List[SimilarImageResult]:
    # TODO: implement it, the AI can't ...
    pass
