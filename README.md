# CloudOps Health API

A small Python service packaged as a non-root Docker container, with liveness and readiness endpoints, Prometheus metrics, and GitHub Actions CI.

## Architecture

```mermaid
flowchart LR
    Client -->|HTTP :8000| API[FastAPI]
    API --> Health[/health and /ready]
    API --> Metrics[/metrics]
    Actions[GitHub Actions] --> Tests[pytest]
    Actions --> Image[Docker build]
```

## Run locally

Requires Python 3.12+.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for interactive API documentation.

## Run with Docker

```bash
docker compose up --build
```

The service listens on `http://localhost:8000`. Stop it with `Ctrl+C`, then run `docker compose down`.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Liveness check |
| GET | `/ready` | Readiness status and process uptime |
| GET | `/metrics` | Prometheus metrics, including request counts |
| GET | `/docs` | Interactive OpenAPI documentation |

## CI checks

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
docker build -t cloudops-health-api:local .
```

GitHub Actions runs the test suite and builds the container on pushes and pull requests to `main`.

## Security notes

The image uses a slim Python base, runs as a dedicated non-root user, excludes local secrets and caches from the build context, and grants the workflow read-only repository permissions. Add deployment secrets through your hosting platform's secret manager; do not commit credentials.

