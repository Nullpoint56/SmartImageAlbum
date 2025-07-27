from datetime import timedelta

from pydantic import HttpUrl
from qdrant_client.http.models import PointStruct
from shared.clients.embedder import EmbeddingRequest
from shared.custom_types.enums import JobStepName

from dependencies import WorkerContext
from executors import step  # Only import decorator, not registry


@step(JobStepName.EMBEDDING)
def run_embed(*, job, step, ctx: WorkerContext, state: dict):
    url = ctx.minio.presigned_get_object(
        bucket_name=ctx.config.object_store.bucket,
        object_name=job.image.object_key,
        expires=timedelta(minutes=15),
    )
    result = ctx.embedder.embed(EmbeddingRequest(image_id=job.image_id, url=HttpUrl(url)))

    job.embedder_model = result.embedder_model
    job.dimension = result.dimension
    state["embedding"] = result.vector


@step(JobStepName.INDEXING)
def run_index(*, job, step, ctx: WorkerContext, state: dict):
    embedding = state["embedding"]
    ctx.qdrant.upsert(
        collection_name=ctx.config.vector_db.collection,
        points=[PointStruct(
            id=str(job.image_id),
            vector=embedding,
            payload={"image_id": str(job.image_id)}
        )]
    )
