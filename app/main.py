import hmac
import json
import logging
import time
import uuid

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app import db, services
from app.config import get_settings
from app.metrics import request_seconds
from app.models import DiagnoseRequest, DiagnoseResponse, IngestResponse

app = FastAPI(title="CloudOps Copilot", version="0.1.0")
logger = logging.getLogger("cloudops")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False


def authorize(x_api_key: str = Header(default="")) -> None:
    expected = get_settings().app_api_key
    if expected and not hmac.compare_digest(x_api_key, expected):
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.middleware("http")
async def instrument(request: Request, call_next):
    request_id = uuid.uuid4().hex
    started = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        elapsed = time.perf_counter() - started
        route = request.scope.get("route")
        route_path = getattr(route, "path", "unmatched")
        request_seconds.labels(request.method, route_path).observe(elapsed)
        logger.info(json.dumps({"request_id": request_id, "method": request.method,
                                "route": route_path, "status": status,
                                "duration_seconds": round(elapsed, 6)}))


@app.get("/livez")
def livez():
    return {"status": "ok"}


@app.get("/healthz")
def healthz():
    try:
        with db.connect() as conn:
            conn.execute("SELECT 1")
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable") from None
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/ingest", response_model=IngestResponse, dependencies=[Depends(authorize)])
def ingest():
    try:
        files, chunks = services.ingest()
    except Exception:
        logger.exception("Runbook ingestion failed")
        raise HTTPException(status_code=503, detail="Runbook ingestion failed; check server logs") from None
    return IngestResponse(files=files, chunks=chunks)


@app.post("/diagnose", response_model=DiagnoseResponse, dependencies=[Depends(authorize)])
def diagnose(body: DiagnoseRequest):
    try:
        return services.diagnose(body.incident)
    except Exception:
        logger.exception("Incident diagnosis failed")
        raise HTTPException(status_code=503, detail="Diagnosis unavailable; check server logs") from None
