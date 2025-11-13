import pytest

pytest.importorskip("fastapi")
from fastapi import FastAPI
from fastapi.testclient import TestClient


def _build_test_client(tmp_path, monkeypatch) -> TestClient:
    """Mount the watchlist router with its file store redirected."""
    import app.api.watchlist as watchlist_mod
    from app.services import database as db_mod

    # Force the API to use the JSON fallback instead of Postgres.
    def _raise_db_error():  # pragma: no cover - defensive helper
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(db_mod, "get_database_service", _raise_db_error)

    data_file = tmp_path / "watchlist.json"
    data_file.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(watchlist_mod, "DATA_FILE", data_file)

    test_app = FastAPI()
    test_app.include_router(watchlist_mod.router)
    return TestClient(test_app)


def test_watchlist_file_fallback_flow(tmp_path, monkeypatch):
    client = _build_test_client(tmp_path, monkeypatch)

    payload = {"ticker": "nvda", "reason": "Breakout", "status": "Watching"}
    res = client.post("/api/watchlist/add", json=payload)
    assert res.status_code == 200
    assert res.json()["ticker"] == "NVDA"

    res = client.get("/api/watchlist")
    body = res.json()
    assert body["total"] == 1
    assert body["items"][0]["ticker"] == "NVDA"
    assert body["items"][0]["status"] == "Watching"

    res = client.delete("/api/watchlist/remove/NVDA")
    assert res.status_code == 200
    assert "removed" in res.json()["message"].lower()

    res = client.get("/api/watchlist")
    assert res.json()["total"] == 0
