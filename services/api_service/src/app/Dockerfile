FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS final

WORKDIR /src

# Copy only project metadata for dependency install
COPY pyproject.toml .

# Install dependencies into system site-packages (required for Docker)
RUN uv pip install -e . --system && python -m pip install alembic

# Copy the source code
COPY . .

# Copy and set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Ensure logs dir exists (optional)
RUN mkdir -p logs

# Set PYTHONPATH so `import app` and `import shared` work
ENV PYTHONPATH=/src

# Use entrypoint script to handle migration + app launch
CMD ["/entrypoint.sh"]
