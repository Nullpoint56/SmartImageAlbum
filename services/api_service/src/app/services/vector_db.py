import uuid
from typing import List

from qdrant_client import AsyncQdrantClient
from qdrant_client.conversions.common_types import PointId
from qdrant_client.http.models import ScoredPoint

from schemas.images import SimilarImageResult

VECTOR_COLLECTION = "image_vectors"

qdrant_client = AsyncQdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)


async def find_similar_images(image_id: uuid.UUID, top_k: int = 5) -> List[SimilarImageResult]:
    # Look up vector by ID
    search_result: List[ScoredPoint] = await qdrant_client.search(
        collection_name=VECTOR_COLLECTION,
        query_vector=PointId(str(image_id)),  # assumes stored under ID
        limit=top_k
    )

    return [
        SimilarImageResult(
            image_id=uuid.UUID(sp.id),
            similarity=sp.score,
            url=sp.payload.get("url", "")
        )
        for sp in search_result
    ]
