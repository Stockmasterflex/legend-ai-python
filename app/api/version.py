from fastapi import APIRouter
import os
import subprocess
import logging

router = APIRouter()


def _resolve_build_sha() -> str:
    for k in ("BUILD_SHA", "GIT_COMMIT", "RAILWAY_GIT_COMMIT_SHA"):
        v = os.getenv(k, "").strip()
        if v:
            return v[:7]
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        logging.getLogger(__name__).info("version: no git sha available")
        return "unknown"


@router.get("/version")
def version():
    return {"build_sha": _resolve_build_sha()}

