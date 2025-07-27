FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS final

WORKDIR /app

# Copy both pyproject + source before installing
COPY src/libraries/shared ./shared
COPY src/services/backend_worker_service/pyproject.toml ./worker/

# Now it's safe to install the shared library
RUN uv pip install ./shared --system

# Install worker service (editable or normal)
RUN uv pip install -e ./worker --system

# Copy worker source code
COPY src/services/backend_worker_service/src ./worker

# Set up import paths
ENV PYTHONPATH=/app/worker:/app/shared

CMD ["python", "-m", "celery", "-A", "app:celery_app", "worker", "--loglevel=INFO"]

