"""Shared test fixtures."""

import pytest

from app.services.market_data import MarketDataService, market_data_service


@pytest.fixture(autouse=True)
def reset_market_data_service():
    """Ensure test overrides on market data service don't leak between tests."""
    market_data_service._get_from_yahoo = MarketDataService._get_from_yahoo.__get__(
        market_data_service, MarketDataService
    )
    yield
