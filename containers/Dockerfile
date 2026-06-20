# Base image for the jansky course: JupyterLab + the core scientific stack.
#
# This is the portable default that runs every notebook except the ones that
# explicitly need CASA (Chapter 12) or GNU Radio/SDR (Chapters 5-6), which have
# their own images. Built on the official uv image so the in-container
# environment matches what you get locally from `uv sync`.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

LABEL org.opencontainers.image.title="jansky" \
      org.opencontainers.image.description="Hands-on radio astronomy course (JupyterLab)" \
      org.opencontainers.image.source="https://github.com/joebarbere/jansky"

# System libraries some scientific wheels expect at runtime.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libgl1 \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Install dependencies first (cached layer), then the project itself.
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev --extra dynamics \
    && uv pip install jupyterlab

# Bring in the rest of the course content.
COPY notebooks ./notebooks
COPY docs ./docs
COPY data ./data

ENV JANSKY_DATA_DIR=/workspace/data
EXPOSE 8888

# Launch JupyterLab with no token for a frictionless local teaching session.
# (Do NOT expose this port to an untrusted network without enabling auth.)
CMD ["uv", "run", "--no-dev", "jupyter", "lab", \
     "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", \
     "--ServerApp.token=", "--ServerApp.password="]
