import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
import pandas as pd
import numpy as np
from app.main import app
from app.services.multitimeframe import get_multitf_service

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_market_data():
    dates = pd.date_range("2024-01-01", periods=100, freq="D")
    return pd.DataFrame({
        "datetime": dates,
        "open": np.linspace(100, 150, 100),
        "high": np.linspace(101, 151, 100),
        "low": np.linspace(99, 149, 100),
        "close": np.linspace(100, 150, 100),
        "volume": np.full(100, 1_000_000),
    })

@patch("app.services.multitimeframe.market_data_service")
@patch("app.core.pattern_detector.PatternDetector")
def test_multitf_analyze_endpoint(mock_detector_cls, mock_market_service, client, mock_market_data):
    # Setup mocks
    mock_market_service.get_time_series = AsyncMock(return_value=mock_market_data)
    
    mock_detector = MagicMock()
    # Mock analyze_ticker to return a dummy result
    mock_analysis = MagicMock()
    mock_analysis.score = 8.0
    mock_analysis.pattern = "VCP"
    mock_analysis.entry = 150.0
    mock_analysis.stop = 140.0
    mock_analysis.target = 170.0
    mock_detector.analyze_ticker = AsyncMock(return_value=mock_analysis)
    
    # We need to mock the detector instance used by the service
    # Since the service is a singleton, we might need to reset it or patch the class used in __init__
    # But get_multitf_service creates a new instance if global is None.
    # Ideally we patch PatternDetector before the service is initialized.
    
    # Let's patch the detector attribute of the service directly if possible, 
    # or rely on the fact that we patched the class before the service might be re-instantiated?
    # Actually, if the service is already instantiated, patching the class won't affect it.
    # So we should patch the service's detector.
    
    with patch("app.services.multitimeframe._multitf_service", None): # Reset singleton
        with patch("app.services.multitimeframe.PatternDetector", return_value=mock_detector):
            response = client.post(
                "/api/multitimeframe/analyze",
                json={"ticker": "AAPL"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["ticker"] == "AAPL"
            assert "confluence" in data
            assert "details" in data
            
            # Verify that analyze_ticker was called 4 times (1D, 1W, 4H, 1H)
            assert mock_detector.analyze_ticker.call_count == 4
            
            # Verify calls arguments to check SPY data usage
            # The calls are likely in order of timeframes list: ["1day", "1week", "4hour", "1hour"]
            # 1day call should have SPY data (which is mock_market_data because we mocked get_time_series)
            # Others should have None for SPY data
            
            calls = mock_detector.analyze_ticker.call_args_list
            
            # Check 1day call (first one)
            args_1d, _ = calls[0]
            assert args_1d[0] == "AAPL"
            # args_1d[2] is spy_data. It should be the dataframe (mock_market_data)
            assert args_1d[2] is not None 
            
            # Check 1week call (second one)
            args_1w, _ = calls[1]
            assert args_1w[2] is None
            
            # Check 4hour call (third one)
            args_4h, _ = calls[2]
            assert args_4h[2] is None

