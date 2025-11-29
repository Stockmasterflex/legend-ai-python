import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import patterns as patterns_api


def _build_client():
    app = FastAPI()
    app.include_router(patterns_api.router)
    return TestClient(app)


@pytest.mark.asyncio
async def test_scan_endpoint(monkeypatch):
    async def fake_scan_with_pattern_engine(*args, **kwargs):
        return {
            "results": [{"ticker": "AAPL", "pattern": "Cup & Handle", "score": 7.2}],
            "errors": {},
            "as_of": "2024-01-01T00:00:00Z",
            "meta": {"duration_ms": 1.0},
        }

    monkeypatch.setattr(
        patterns_api.pattern_scanner_service,
        "scan_with_pattern_engine",
        fake_scan_with_pattern_engine,
    )

    client = _build_client()
    response = client.post(
        "/api/patterns/scan",
        json={
            "tickers": ["AAPL"],
            "interval": "1day",
            "apply_filters": True,
            "min_score": 6.0,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["results"][0]["ticker"] == "AAPL"


def test_filter_endpoint():
    client = _build_client()
    response = client.post(
        "/api/patterns/filter",
        json={
            "patterns": [
                {"ticker": "AAPL", "current_price": 150},
                {"ticker": "LOW", "current_price": 20},
            ],
            "filter_config": {"min_price": 30},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["results"][0]["ticker"] == "AAPL"


def test_score_endpoint():
    client = _build_client()
    response = client.post(
        "/api/patterns/score",
        json={
            "pattern": {
                "ticker": "AAPL",
                "current_price": 55,
                "pattern_height_pct": 0.12,
                "metadata": {"year_high": 60, "year_low": 30, "base_depth_pct": 0.12},
            }
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["score"] > 0
    assert "components" in body


def test_export_endpoint(tmp_path):
    client = _build_client()
    response = client.post(
        "/api/patterns/export",
        json={
            "patterns": [{"ticker": "AAPL", "pattern": "Cup", "score": 7.5}],
            "format": "json",
            "output_dir": str(tmp_path),
            "filename": "export.json",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True

    # Ensure file is actually written
    path = tmp_path / "export.json"
    assert path.exists()


def test_catalog_endpoint():
    client = _build_client()
    response = client.get("/api/patterns/catalog")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    names = [item["name"] for item in body["patterns"]]
    assert "MMU VCP" in names
