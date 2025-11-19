"""
Tests for crypto analysis features
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from app.services.crypto_data import BinanceClient, CoinGeckoClient, CoinbaseClient, CryptoDataService
from app.services.crypto_patterns import WhaleMovementDetector, FundingRateAnalyzer, OpenInterestAnalyzer
from app.services.correlation_analysis import CorrelationCalculator, BitcoinDominanceTracker
from app.services.defi_analytics import LiquidityPoolAnalyzer, GasOptimizer


class TestCryptoDataSources:
    """Test crypto data source integrations"""

    @pytest.mark.asyncio
    async def test_binance_client_price(self):
        """Test Binance price fetching"""
        client = BinanceClient()

        with patch.object(client.client, 'get') as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: {"symbol": "BTCUSDT", "price": "43250.50"}
            )

            result = await client.get_ticker_price("BTCUSDT")

            assert result is not None
            assert result["symbol"] == "BTCUSDT"
            assert "price" in result

        await client.close()

    @pytest.mark.asyncio
    async def test_binance_klines(self):
        """Test Binance klines data"""
        client = BinanceClient()

        with patch.object(client.client, 'get') as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: [
                    [1609459200000, "29000", "29500", "28500", "29200", "1000", 0, "29100000", 100],
                    [1609545600000, "29200", "30000", "29000", "29800", "1200", 0, "35760000", 120]
                ]
            )

            result = await client.get_klines("BTCUSDT", "1d", 2)

            assert result is not None
            assert len(result) == 2
            assert all(k in result[0] for k in ["t", "o", "h", "l", "c", "v"])

        await client.close()

    @pytest.mark.asyncio
    async def test_coingecko_price(self):
        """Test CoinGecko price fetching"""
        client = CoinGeckoClient()

        with patch.object(client.client, 'get') as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: {
                    "bitcoin": {
                        "usd": 43250.50,
                        "usd_market_cap": 845000000000,
                        "usd_24h_vol": 28000000000,
                        "usd_24h_change": 2.5
                    }
                }
            )

            result = await client.get_price("bitcoin", "usd")

            assert result is not None
            assert "bitcoin" in result
            assert result["bitcoin"]["usd"] == 43250.50

        await client.close()

    @pytest.mark.asyncio
    async def test_crypto_data_service_fallback(self):
        """Test CryptoDataService multi-source fallback"""
        service = CryptoDataService()

        with patch.object(service.binance, 'get_ticker_price') as mock_binance:
            mock_binance.return_value = {"symbol": "BTCUSDT", "price": "43250.50"}

            result = await service.get_realtime_price("BTC", "USDT")

            assert result is not None
            assert result["symbol"] == "BTC"
            assert result["price"] == 43250.50
            assert result["source"] == "binance"

        await service.close()


class TestCryptoPatterns:
    """Test crypto-specific pattern detection"""

    @pytest.mark.asyncio
    async def test_whale_detection(self):
        """Test whale movement detection"""
        detector = WhaleMovementDetector()

        # Mock klines data with volume spike
        mock_klines = []
        for i in range(24):
            mock_klines.append({
                "t": 1609459200000 + i * 3600000,
                "o": 43000 + i * 10,
                "h": 43100 + i * 10,
                "l": 42900 + i * 10,
                "c": 43050 + i * 10,
                "v": 1000 if i < 23 else 5000,  # Volume spike at the end
                "qv": 43050000
            })

        with patch('app.services.crypto_data.crypto_data_service') as mock_service:
            mock_service.binance.get_klines = AsyncMock(return_value=mock_klines)

            result = await detector.detect_whale_activity("BTCUSDT", 24)

            assert result is not None
            assert "whale_detected" in result
            assert "volume_spike" in result
            assert "sentiment" in result

    @pytest.mark.asyncio
    async def test_funding_rate_analysis(self):
        """Test funding rate analysis"""
        analyzer = FundingRateAnalyzer()

        with patch('app.services.crypto_data.crypto_data_service') as mock_service:
            # Mock extreme positive funding rate
            mock_service.binance.get_funding_rate = AsyncMock(return_value={
                "symbol": "BTCUSDT",
                "fundingRate": "0.001",  # 0.1% per 8h = ~10.95% annualized
                "fundingTime": 1609459200000
            })

            result = await analyzer.analyze_funding_rate("BTCUSDT")

            assert result is not None
            assert result["symbol"] == "BTCUSDT"
            assert "funding_rate_annualized" in result
            assert result["sentiment"] == "bullish"  # Positive funding
            assert "signal" in result

    @pytest.mark.asyncio
    async def test_open_interest_analysis(self):
        """Test open interest analysis"""
        analyzer = OpenInterestAnalyzer()

        mock_klines = []
        for i in range(24):
            mock_klines.append({
                "t": 1609459200000 + i * 3600000,
                "o": 43000,
                "h": 43100,
                "l": 42900,
                "c": 43050 + i * 50,  # Rising price
                "v": 1000 + i * 100,  # Increasing volume
                "qv": 43050000
            })

        with patch('app.services.crypto_data.crypto_data_service') as mock_service:
            mock_service.binance.get_open_interest = AsyncMock(return_value={
                "symbol": "BTCUSDT",
                "openInterest": "125000"
            })
            mock_service.binance.get_klines = AsyncMock(return_value=mock_klines)

            result = await analyzer.analyze_open_interest("BTCUSDT", 24)

            assert result is not None
            assert result["symbol"] == "BTCUSDT"
            assert "current_oi" in result
            assert "trend" in result


class TestCorrelationAnalysis:
    """Test cross-asset correlation analysis"""

    def test_correlation_calculator(self):
        """Test correlation calculation"""
        calc = CorrelationCalculator()

        series1 = [1, 2, 3, 4, 5]
        series2 = [2, 4, 6, 8, 10]  # Perfect positive correlation

        corr = calc.calculate_correlation(series1, series2)

        assert corr is not None
        assert abs(corr - 1.0) < 0.01  # Should be close to 1.0

    def test_rolling_correlation(self):
        """Test rolling correlation"""
        calc = CorrelationCalculator()

        series1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        series2 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

        rolling = calc.calculate_rolling_correlation(series1, series2, window=5)

        assert len(rolling) > 0
        assert all(abs(r - 1.0) < 0.01 for r in rolling)  # All should be ~1.0

    @pytest.mark.asyncio
    async def test_btc_dominance(self):
        """Test Bitcoin dominance tracking"""
        tracker = BitcoinDominanceTracker()

        with patch('app.services.crypto_data.crypto_data_service') as mock_service:
            mock_service.coingecko.get_global_market_data = AsyncMock(return_value={
                "market_cap_percentage": {
                    "btc": 52.5,
                    "eth": 17.2
                }
            })

            mock_klines = [
                {"c": 43000 + i * 100, "o": 43000 + i * 100} for i in range(30)
            ]
            mock_service.binance.get_klines = AsyncMock(return_value=mock_klines)

            result = await tracker.get_bitcoin_dominance()

            assert result is not None
            assert result["btc_dominance"] == 52.5
            assert result["eth_dominance"] == 17.2
            assert "regime" in result
            assert "signal" in result


class TestDeFiAnalytics:
    """Test DeFi analytics features"""

    @pytest.mark.asyncio
    async def test_gas_optimizer(self):
        """Test gas price optimization"""
        optimizer = GasOptimizer()

        with patch.object(optimizer.client, 'get') as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: {
                    "result": {
                        "SafeGasPrice": "25",
                        "ProposeGasPrice": "30",
                        "FastGasPrice": "35"
                    }
                }
            )

            result = await optimizer.get_gas_prices("ethereum")

            assert result is not None
            assert result["standard"] == 30
            assert result["fast"] == 35
            assert "recommendation" in result

        await optimizer.close()

    @pytest.mark.asyncio
    async def test_transaction_cost_estimation(self):
        """Test transaction cost estimation"""
        optimizer = GasOptimizer()

        result = await optimizer.estimate_transaction_cost(
            gas_limit=21000,
            gas_price_gwei=30,
            eth_price_usd=4000
        )

        assert result is not None
        assert result["gas_limit"] == 21000
        assert result["gas_price_gwei"] == 30
        assert "cost_eth" in result
        assert "cost_usd" in result

        await optimizer.close()

    @pytest.mark.asyncio
    async def test_impermanent_loss_calculation(self):
        """Test impermanent loss calculation"""
        analyzer = LiquidityPoolAnalyzer()

        result = await analyzer.calculate_impermanent_loss(
            initial_price_ratio=1.0,
            current_price_ratio=2.0,
            initial_amount_a=1.0,
            initial_amount_b=1.0
        )

        assert result is not None
        assert "il_percentage" in result
        assert "value_if_held" in result
        assert "value_in_pool" in result
        assert result["il_percentage"] < 0  # IL should be negative

        await analyzer.close()


@pytest.mark.asyncio
async def test_crypto_api_price_endpoint():
    """Test crypto API price endpoint"""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    with patch('app.services.crypto_data.crypto_data_service') as mock_service:
        mock_service.get_realtime_price = AsyncMock(return_value={
            "symbol": "BTC",
            "price": 43250.50,
            "source": "binance",
            "timestamp": 1609459200
        })

        response = client.get("/crypto/price/BTC?quote_currency=USDT")

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "BTC"
        assert data["price"] == 43250.50


@pytest.mark.asyncio
async def test_crypto_api_patterns_endpoint():
    """Test crypto API patterns endpoint"""
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    with patch('app.services.crypto_patterns.crypto_pattern_analyzer') as mock_analyzer:
        mock_analyzer.analyze_comprehensive = AsyncMock(return_value={
            "symbol": "BTCUSDT",
            "whale_activity": {"whale_detected": False},
            "overall_signal": "neutral",
            "confidence": 0.5,
            "risk_level": "low",
            "recommendations": []
        })

        response = client.get("/crypto/patterns/BTCUSDT?lookback_hours=24")

        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "BTCUSDT"
        assert "overall_signal" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
