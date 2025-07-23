import httpx

async def download_image(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.content

async def embed_image(image_bytes: bytes) -> list[float]:
    # This will call the embedding service later
    # raise NotImplementedError("Embedding service call not implemented")
    print("Embedded")

async def store_vector(job_id: str, embedding: list[float]) -> None:
    # This will store the vector into Qdrant or similar
    # raise NotImplementedError("Vector DB integration not implemented")
    print("Stored")
