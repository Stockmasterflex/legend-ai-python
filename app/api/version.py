from fastapi import APIRouter, Request

from app.utils.build_info import resolve_build_payload

router = APIRouter()


@router.get("/api/version")
def api_version(request: Request):
    """Detailed version payload for API clients."""
    request.state.telemetry = {"event": "version_api", "status": 200}
    return resolve_build_payload()


@router.get("/version")
def version_plain(request: Request):
    """Shallow version payload for cache-busting and health checks."""
    payload = resolve_build_payload()
    request.state.telemetry = {"event": "version_plain", "status": 200}
    return {"build_sha": payload["build_sha"], "version": payload["version"]}
