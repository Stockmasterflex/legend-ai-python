from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
def metrics_endpoint():
    """Expose Prometheus metrics collected in-process."""
    payload = generate_latest()
    return Response(content=payload, media_type=CONTENT_TYPE_LATEST)
