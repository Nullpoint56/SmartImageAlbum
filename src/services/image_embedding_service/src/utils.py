import aiohttp
from fastapi import HTTPException


async def get_image_bytes(image_url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status != 200:
                raise HTTPException(status_code=400, detail="Failed to download image")
            return await response.read()

