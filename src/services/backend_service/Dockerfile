FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS final

WORKDIR /app

# Copy code
COPY src/libraries/shared ./shared
COPY src/services/backend_service/pyproject.toml ./backend/

# Install
RUN uv pip install ./shared --system
RUN uv pip install -e ./backend --system

COPY src/services/backend_service/src ./backend

# Entrypoint
COPY src/services/backend_service/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Python import roots
ENV PYTHONPATH=/app/backend:/app/shared

# Run entrypoint (note: alembic.ini lives inside backend)
CMD ["./entrypoint.sh"]

