from __future__ import annotations

import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest

STARTED_AT = time.time()
HTTP_REQUESTS = Counter("http_requests_total", "HTTP requests served", ["method", "path", "status"])
APP_UP = Gauge("app_up", "Whether the application is ready")
APP_UP.set(1)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    APP_UP.set(1)
    yield
    APP_UP.set(0)


app = FastAPI(
    title="CloudOps Health API",
    description="A container-ready Python service with health endpoints and Prometheus metrics.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def count_requests(request, call_next):
    response = await call_next(request)
    HTTP_REQUESTS.labels(request.method, request.url.path, str(response.status_code)).inc()
    return response


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready", tags=["health"])
def ready() -> dict[str, str | int]:
    return {"status": "ready", "uptime_seconds": int(time.time() - STARTED_AT)}


@app.get("/metrics", tags=["observability"])
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

