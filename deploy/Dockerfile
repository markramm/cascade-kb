# =============================================================================
# Stage 1: Build Svelte viewer
# =============================================================================
FROM node:22-alpine AS viewer-build

WORKDIR /build/viewer
COPY viewer/package.json viewer/package-lock.json ./
RUN npm ci --legacy-peer-deps
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

# Clone and install pyrite from a specific release tag
ARG PYRITE_VERSION=v0.21.0
RUN git clone --branch $PYRITE_VERSION --depth=1 https://github.com/markramm/pyrite.git /tmp/pyrite && \
    cd /tmp/pyrite && \
    pip install --no-cache-dir ".[server,ai,cli]" && \
    pip install --no-cache-dir ".[semantic]" && \
    pip install --no-cache-dir /tmp/pyrite/extensions/journalism-investigation && \
    pip install --no-cache-dir /tmp/pyrite/extensions/cascade && \
    rm -rf /tmp/pyrite

RUN apt-get purge -y build-essential gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy KB data for seeding
COPY cascade-timeline/ /seed/cascade-timeline/

# Copy built viewer
COPY --from=viewer-build /build/viewer/build/ /app/viewer-dist/

# Copy deploy scripts
COPY deploy/seed.sh /app/seed.sh
RUN chmod +x /app/seed.sh

# Create non-root user
RUN useradd --create-home --shell /bin/bash pyrite

ENV PYRITE_DATA_DIR=/data
RUN mkdir -p /data && chown pyrite:pyrite /data
VOLUME /data

USER pyrite

EXPOSE 8088

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8088/health')" || exit 1

CMD ["pyrite-server"]
