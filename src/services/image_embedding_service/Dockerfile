FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS final

WORKDIR /app

# Copy shared library first
COPY src/libraries/shared ./shared
COPY src/services/image_embedding_service ./embedder

# Now it's safe to install the shared library
RUN uv pip install ./shared --system

# Install embedder service (regular mode, not -e)
RUN uv pip install -e ./embedder --system

# Copy embedder source code
COPY src/services/image_embedding_service/src ./embedder

# Set import paths and model caching
ENV PYTHONPATH=/app/embedder:/app/shared
ENV TRANSFORMERS_NO_TF=1
ENV TRANSFORMERS_CACHE=/app/.cache

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
