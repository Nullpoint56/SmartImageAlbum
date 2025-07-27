FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS final

# Install system dependencies for image processing
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only dependency metadata
COPY src/services/image_embedding_service/pyproject.toml ./pyproject.toml

# Install all dependencies into system site-packages (required for uv + Docker)
RUN uv pip install . --system

# Copy the actual source code
COPY src/services/image_embedding_service/src ./src

# Set environment variables
ENV PYTHONPATH=/app/src
ENV TRANSFORMERS_NO_TF=1
ENV TRANSFORMERS_CACHE=/app/.cache

# Run the FastAPI app via uvicorn (as a module to ensure correct loading)
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
