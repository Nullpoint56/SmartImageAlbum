import httpx

from pydantic import HttpUrl


async def notify_coordinator(url: HttpUrl):
    async with httpx.AsyncClient() as client:
        try:
            job_id = await client.post("http://coordinator:8001/jobs", json={"image_url": url})
        except httpx.RequestError as e:
            print(f"Failed to notify coordinator: {e}")