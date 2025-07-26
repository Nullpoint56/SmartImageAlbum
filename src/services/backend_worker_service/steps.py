from datetime import timedelta

from pydantic import HttpUrl

from executors import step
from shared.clients.embedder import EmbeddingRequest
from shared.custom_types.enums import JobStepName


@step(JobStepName.EMBEDDING)
def run_embed(*, job, deps):
    url = deps.minio.presigned_get_object("uploads", job.image.object_key, timedelta(minutes=15))
    result = deps.embedder.embed(EmbeddingRequest(image_id=job.image_id, url=HttpUrl(url)))
    job.embedding = result.embedding
    job.embedder_model = result.embedder_model
    job.dimension = result.dimension


@step(JobStepName.INDEXING)
def run_index(*, job, deps):
    deps.qdrant.upsert(
        image_id=job.image_id,
        embedding=job.embedding,
        metadata={"embedder_model": job.embedder_model}
    )
