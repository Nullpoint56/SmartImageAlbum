# worker/Dockerfile

FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS final

WORKDIR /src

# Copy only the necessary pyproject + lock files for dependency resolution
COPY src/shared/pyproject.toml src/shared/uv.lock ./shared/
COPY src/worker/pyproject.toml src/worker/uv.lock ./worker/

# Install dependencies
RUN uv pip install -r ./shared/pyproject.toml --system
RUN uv pip install -e ./worker --system

# Copy only the needed source code (shared + worker)
COPY src/shared ./shared
COPY src/worker ./worker

# Ensure imports like `from shared...` work
ENV PYTHONPATH=/src

CMD ["celery", "-A", "worker.app.celery_app", "worker", "--loglevel=INFO"]
