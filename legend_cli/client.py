"""API client for Legend AI backend."""

import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime


class LegendAPIClient:
    """Client for interacting with Legend AI API."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_key: Optional[str] = None,
        timeout: int = 30
    ):
        """Initialize API client."""
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout

        headers = {}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def close(self):
        """Close the client."""
        await self.client.aclose()

    # Health & Status
    async def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        response = await self.client.get('/health')
        response.raise_for_status()
        return response.json()

    # Analysis
    async def analyze(
        self,
        ticker: str,
        interval: str = "1day",
        bars: int = 400
    ) -> Dict[str, Any]:
        """Analyze a ticker."""
        response = await self.client.get(
            '/api/analyze',
            params={'ticker': ticker, 'interval': interval, 'bars': bars}
        )
        response.raise_for_status()
        return response.json()

    async def analyze_pattern(
        self,
        ticker: str,
        interval: str = "1day"
    ) -> Dict[str, Any]:
        """Detect patterns for a ticker."""
        response = await self.client.get(
            '/api/patterns/detect',
            params={'ticker': ticker, 'interval': interval}
        )
        response.raise_for_status()
        return response.json()

    # Scanning
    async def scan(
        self,
        universe: str = "SP500",
        sector: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_volume: Optional[int] = None,
        pattern_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Scan universe for patterns."""
        params = {'universe': universe}

        if sector:
            params['sector'] = sector
        if min_price is not None:
            params['min_price'] = min_price
        if max_price is not None:
            params['max_price'] = max_price
        if min_volume is not None:
            params['min_volume'] = min_volume
        if pattern_types:
            params['pattern_types'] = ','.join(pattern_types)

        response = await self.client.get('/api/scan', params=params)
        response.raise_for_status()
        return response.json()

    async def quick_scan(self, universe: str = "SP500") -> Dict[str, Any]:
        """Quick universe scan."""
        response = await self.client.get(
            f'/api/universe/scan/quick',
            params={'universe': universe}
        )
        response.raise_for_status()
        return response.json()

    # Market Analysis
    async def market_internals(self, universe: str = "SP500") -> Dict[str, Any]:
        """Get market internals analysis."""
        response = await self.client.get(
            '/api/market/internals',
            params={'universe': universe}
        )
        response.raise_for_status()
        return response.json()

    # Watchlist
    async def watchlist_add(
        self,
        ticker: str,
        notes: Optional[str] = None,
        alert_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """Add ticker to watchlist."""
        payload = {'ticker': ticker}
        if notes:
            payload['notes'] = notes
        if alert_price is not None:
            payload['alert_price'] = alert_price

        response = await self.client.post('/api/watchlist/add', json=payload)
        response.raise_for_status()
        return response.json()

    async def watchlist_remove(self, ticker: str) -> Dict[str, Any]:
        """Remove ticker from watchlist."""
        response = await self.client.delete(f'/api/watchlist/remove/{ticker}')
        response.raise_for_status()
        return response.json()

    async def watchlist_list(self, status: Optional[str] = None) -> Dict[str, Any]:
        """List watchlist items."""
        params = {}
        if status:
            params['status'] = status

        response = await self.client.get('/api/watchlist', params=params)
        response.raise_for_status()
        return response.json()

    async def watchlist_update_status(
        self,
        ticker: str,
        status: str
    ) -> Dict[str, Any]:
        """Update watchlist item status."""
        response = await self.client.patch(
            f'/api/watchlist/{ticker}/status',
            json={'status': status}
        )
        response.raise_for_status()
        return response.json()

    # Charts
    async def generate_chart(
        self,
        ticker: str,
        interval: str = "1day",
        bars: int = 120
    ) -> Dict[str, Any]:
        """Generate chart for ticker."""
        response = await self.client.get(
            '/api/charts/generate',
            params={'ticker': ticker, 'interval': interval, 'bars': bars}
        )
        response.raise_for_status()
        return response.json()

    # Alerts
    async def alerts_list(
        self,
        ticker: Optional[str] = None,
        active_only: bool = True
    ) -> Dict[str, Any]:
        """List alerts."""
        params = {'active_only': active_only}
        if ticker:
            params['ticker'] = ticker

        response = await self.client.get('/api/alerts', params=params)
        response.raise_for_status()
        return response.json()

    async def alerts_create(
        self,
        ticker: str,
        alert_type: str,
        target_price: Optional[float] = None,
        condition: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create an alert."""
        payload = {
            'ticker': ticker,
            'alert_type': alert_type
        }
        if target_price is not None:
            payload['target_price'] = target_price
        if condition:
            payload['condition'] = condition

        response = await self.client.post('/api/alerts/create', json=payload)
        response.raise_for_status()
        return response.json()

    async def alerts_delete(self, alert_id: int) -> Dict[str, Any]:
        """Delete an alert."""
        response = await self.client.delete(f'/api/alerts/{alert_id}')
        response.raise_for_status()
        return response.json()

    # Trades
    async def trades_list(
        self,
        status: Optional[str] = None,
        ticker: Optional[str] = None
    ) -> Dict[str, Any]:
        """List trades."""
        params = {}
        if status:
            params['status'] = status
        if ticker:
            params['ticker'] = ticker

        response = await self.client.get('/api/trades', params=params)
        response.raise_for_status()
        return response.json()

    async def trades_create(
        self,
        ticker: str,
        entry_price: float,
        position_size: int,
        stop_loss: Optional[float] = None,
        target: Optional[float] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a trade."""
        payload = {
            'ticker': ticker,
            'entry_price': entry_price,
            'position_size': position_size
        }
        if stop_loss is not None:
            payload['stop_loss'] = stop_loss
        if target is not None:
            payload['target'] = target
        if notes:
            payload['notes'] = notes

        response = await self.client.post('/api/trades/create', json=payload)
        response.raise_for_status()
        return response.json()

    async def trades_close(
        self,
        trade_id: int,
        exit_price: float,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Close a trade."""
        payload = {'exit_price': exit_price}
        if notes:
            payload['notes'] = notes

        response = await self.client.post(
            f'/api/trades/{trade_id}/close',
            json=payload
        )
        response.raise_for_status()
        return response.json()

    # Risk Management
    async def calculate_risk(
        self,
        account_size: float,
        risk_percent: float,
        entry_price: float,
        stop_loss: float
    ) -> Dict[str, Any]:
        """Calculate position size and risk."""
        response = await self.client.get(
            '/api/risk/calculate',
            params={
                'account_size': account_size,
                'risk_percent': risk_percent,
                'entry_price': entry_price,
                'stop_loss': stop_loss
            }
        )
        response.raise_for_status()
        return response.json()

    # AI Assistant
    async def ai_chat(self, message: str) -> Dict[str, Any]:
        """Chat with AI assistant."""
        response = await self.client.post(
            '/api/ai/chat',
            json={'message': message}
        )
        response.raise_for_status()
        return response.json()

    async def ai_analyze(self, ticker: str) -> Dict[str, Any]:
        """Get AI analysis for ticker."""
        response = await self.client.get(
            '/api/ai/analyze',
            params={'ticker': ticker}
        )
        response.raise_for_status()
        return response.json()
