# =============================================================================
# Stage 1: Build React viewer
# =============================================================================
FROM node:22-alpine AS viewer-build

WORKDIR /build/viewer
COPY viewer/package.json viewer/package-lock.json ./
RUN npm ci
COPY viewer/ ./
RUN npm run build

# =============================================================================
# Stage 2: Pyrite + KB data + built viewer
# =============================================================================
FROM python:3.12-slim AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc git \
    && rm -rf /var/lib/apt/lists/*

# Install pyrite from PyPI (or local if needed)
RUN pip install --no-cache-dir "pyrite-kb[server,ai,cli,semantic]"

RUN apt-get purge -y build-essential gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy KB data for seeding
COPY cascade-timeline/ /seed/cascade-timeline/

# Copy built viewer
COPY --from=viewer-build /build/viewer/dist/ /app/viewer-dist/

# Copy deploy scripts
COPY deploy/seed.sh /app/seed.sh
RUN chmod +x /app/seed.sh

# Create non-root user
RUN useradd --create-home --shell /bin/bash pyrite

ENV PYRITE_DATA_DIR=/data
ENV PYRITE_STATIC_DIR=/app/viewer-dist
RUN mkdir -p /data && chown pyrite:pyrite /data
VOLUME /data

USER pyrite

EXPOSE 8088

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8088/health')" || exit 1

CMD ["pyrite-server"]
