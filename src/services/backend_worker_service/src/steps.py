from datetime import timedelta

from pydantic import HttpUrl
from qdrant_client.http.models import PointStruct
from shared.custom_types.enums import JobStepName
from shared.custom_types.schemas import EmbeddingRequest

from dependencies import WorkerContext


def run_embed(job, ctx: WorkerContext, state: dict):
    """Download image from MinIO, call embedding service, and update model metadata."""
    object_key = job.image.object_key

    # Step 1: Get presigned URL for embedding request
    url = ctx.minio.presigned_get_object(
        bucket_name=ctx.config.object_store.bucket,
        object_name=object_key,
        expires=timedelta(minutes=15),
    )

    # Step 2: Get image size via stat_object
    stat = ctx.minio.stat_object(
        bucket_name=ctx.config.object_store.bucket,
        object_name=object_key,
    )
    image_size = stat.size  # in bytes

    # Step 3: Send to embedder
    result = ctx.embedder.embed(
        EmbeddingRequest(image_id=job.image_id, url=HttpUrl(url))
    )

    # Step 4: Update job tracking fields
    job.embedder_model = result.model_name
    job.dimension = result.dimension

    # Step 5: Update ImageMetadata
    if job.image.image_metadata is not None:
        metadata = job.image.image_metadata
        metadata.embedding_model = result.model_name
        metadata.size_bytes = image_size
        ctx.db.add(metadata)

    # Step 6: Save changes to DB
    ctx.db.commit()

    # Step 7: Store embedding in pipeline state
    state["embedding"] = result.embedding



def run_index(job, ctx: WorkerContext, state: dict):
    embedding = state["embedding"]
    ctx.qdrant.upsert(
        collection_name=ctx.config.vector_db.collection,
        points=[PointStruct(
            id=str(job.image_id),
            vector=embedding,
            payload={"image_id": str(job.image_id)}
        )]
    )
