from fastapi import FastAPI

app = FastAPI(title="API Service", version="1.0")

app.include_router(images_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
