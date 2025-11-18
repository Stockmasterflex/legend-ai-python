"""
Correlation Analysis API Endpoints

Provides endpoints for:
- Correlation heatmaps
- Pair trading opportunities
- Portfolio diversification analysis
- Market leadership identification
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import logging

from app.services.correlation_analysis import CorrelationAnalysisService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/correlation", tags=["correlation"])

# Initialize service
correlation_service = CorrelationAnalysisService()


# Request/Response Models

class CorrelationHeatmapRequest(BaseModel):
    """Request model for correlation heatmap."""
    tickers: List[str] = Field(..., description="List of ticker symbols", min_items=2)
    period: str = Field("3month", description="Time period (1month, 3month, 6month, 1year)")
    interval: str = Field("1day", description="Data interval (1day, 1hour)")
    method: str = Field("pearson", description="Correlation method (pearson, spearman, kendall)")


class PairTradingRequest(BaseModel):
    """Request model for pair trading analysis."""
    tickers: List[str] = Field(..., description="List of ticker symbols", min_items=2)
    period: str = Field("3month", description="Historical period for analysis")
    min_correlation: float = Field(0.7, ge=0.0, le=1.0, description="Minimum correlation threshold")
    max_correlation: float = Field(0.95, ge=0.0, le=1.0, description="Maximum correlation threshold")
    top_n: int = Field(20, ge=1, le=100, description="Number of top pairs to return")


class PortfolioDiversificationRequest(BaseModel):
    """Request model for portfolio diversification analysis."""
    portfolio: Dict[str, float] = Field(..., description="Portfolio holdings {ticker: weight}")
    period: str = Field("3month", description="Historical period for analysis")


class MarketLeadershipRequest(BaseModel):
    """Request model for market leadership analysis."""
    tickers: List[str] = Field(..., description="List of ticker symbols")
    benchmark: str = Field("SPY", description="Market benchmark symbol")
    period: str = Field("3month", description="Historical period for analysis")


# API Endpoints

@router.post("/heatmap")
async def get_correlation_heatmap(request: CorrelationHeatmapRequest):
    """
    Generate correlation heatmap for multiple tickers.

    Returns correlation matrix with interactive heatmap data including:
    - Real-time correlations between all ticker pairs
    - Color-coded correlation strength
    - Sector groupings (if applicable)
    - Interactive hover data

    **Example Request:**
    ```json
    {
        "tickers": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
        "period": "3month",
        "interval": "1day",
        "method": "pearson"
    }
    ```
    """
    try:
        result = await correlation_service.get_correlation_heatmap(
            tickers=request.tickers,
            period=request.period,
            interval=request.interval,
            method=request.method
        )

        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        logger.error(f"Error in correlation heatmap endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pair-trading")
async def find_pair_trading_opportunities(request: PairTradingRequest):
    """
    Find correlated pairs suitable for pair trading.

    Analyzes correlations to identify:
    - Highly correlated stock pairs
    - Current spread divergence from mean
    - Mean reversion trading signals
    - Historical spread patterns
    - Lead-lag relationships

    **Trading Signals:**
    - `long_spread`: Spread too low, expect mean reversion (buy ticker1, short ticker2)
    - `short_spread`: Spread too high, expect mean reversion (short ticker1, buy ticker2)
    - `null`: No signal, spread within normal range

    **Example Request:**
    ```json
    {
        "tickers": ["XLE", "XLF", "XLK", "XLV", "XLI", "XLP", "XLY"],
        "period": "3month",
        "min_correlation": 0.7,
        "max_correlation": 0.95,
        "top_n": 10
    }
    ```
    """
    try:
        if request.min_correlation >= request.max_correlation:
            raise HTTPException(
                status_code=400,
                detail="min_correlation must be less than max_correlation"
            )

        result = await correlation_service.find_pair_trading_opportunities(
            tickers=request.tickers,
            period=request.period,
            min_correlation=request.min_correlation,
            max_correlation=request.max_correlation,
            top_n=request.top_n
        )

        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])

        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in pair trading endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio-diversification")
async def analyze_portfolio_diversification(request: PortfolioDiversificationRequest):
    """
    Analyze correlation and diversification of a portfolio.

    Provides comprehensive portfolio analysis including:
    - Average correlation between holdings
    - Weighted correlation metrics
    - Redundant holdings identification (highly correlated pairs)
    - Diversification score (0-1, higher is better)
    - Suggestions for improving diversification
    - Risk clustering analysis

    **Example Request:**
    ```json
    {
        "portfolio": {
            "AAPL": 0.20,
            "MSFT": 0.15,
            "GOOGL": 0.15,
            "AMZN": 0.10,
            "TSLA": 0.10,
            "JPM": 0.15,
            "XOM": 0.15
        },
        "period": "3month"
    }
    ```

    **Note:** Weights should sum to 1.0 (100%)
    """
    try:
        # Validate portfolio weights
        total_weight = sum(request.portfolio.values())
        if not (0.99 <= total_weight <= 1.01):
            logger.warning(f"Portfolio weights sum to {total_weight}, expected 1.0")

        if len(request.portfolio) < 2:
            raise HTTPException(
                status_code=400,
                detail="Portfolio must contain at least 2 holdings"
            )

        result = await correlation_service.analyze_portfolio_diversification(
            portfolio=request.portfolio,
            period=request.period
        )

        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])

        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in portfolio diversification endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/market-leadership")
async def analyze_market_leadership(request: MarketLeadershipRequest):
    """
    Identify which tickers lead or lag the market.

    Analyzes market leadership through:
    - **Beta analysis**: Sensitivity to market movements
    - **Lead-lag detection**: Which stocks move before/after the market
    - **Sector rotation**: Identify leading sectors
    - **Correlation strength**: How closely stocks track the market

    **Leadership Types:**
    - `leader`: Tends to move before the benchmark
    - `laggard`: Tends to follow benchmark movements
    - `simultaneous`: Moves together with the benchmark

    **Beta Interpretation:**
    - Beta > 1.0: More volatile than market
    - Beta ≈ 1.0: Similar volatility to market
    - Beta < 1.0: Less volatile than market
    - Beta < 0: Inverse relationship with market

    **Example Request:**
    ```json
    {
        "tickers": ["AAPL", "MSFT", "TSLA", "JPM", "XOM"],
        "benchmark": "SPY",
        "period": "3month"
    }
    ```
    """
    try:
        result = await correlation_service.analyze_market_leadership(
            tickers=request.tickers,
            benchmark=request.benchmark,
            period=request.period
        )

        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])

        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in market leadership endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quick-correlation")
async def get_quick_correlation(
    ticker1: str = Query(..., description="First ticker symbol"),
    ticker2: str = Query(..., description="Second ticker symbol"),
    period: str = Query("3month", description="Time period"),
    method: str = Query("pearson", description="Correlation method")
):
    """
    Quick correlation check between two tickers.

    Simplified endpoint for checking correlation between just two tickers.
    Returns correlation coefficient and basic relationship info.

    **Example:**
    ```
    GET /api/correlation/quick-correlation?ticker1=AAPL&ticker2=MSFT&period=3month
    ```
    """
    try:
        result = await correlation_service.get_correlation_heatmap(
            tickers=[ticker1, ticker2],
            period=period,
            interval="1day",
            method=method
        )

        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])

        # Extract the correlation between the two tickers
        corr_matrix = result.get('correlation_matrix', {})
        correlation = corr_matrix.get(ticker1, {}).get(ticker2, None)

        if correlation is None:
            raise HTTPException(status_code=404, detail="Correlation not found")

        # Determine relationship strength
        abs_corr = abs(correlation)
        if abs_corr > 0.7:
            strength = "strong"
        elif abs_corr > 0.3:
            strength = "moderate"
        else:
            strength = "weak"

        direction = "positive" if correlation > 0 else "negative"

        return {
            "success": True,
            "data": {
                "ticker1": ticker1,
                "ticker2": ticker2,
                "correlation": correlation,
                "abs_correlation": abs_corr,
                "relationship": f"{strength} {direction}",
                "period": period,
                "method": method,
                "interpretation": _interpret_correlation(correlation)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in quick correlation endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Helper functions

def _interpret_correlation(corr: float) -> str:
    """Generate human-readable interpretation of correlation."""
    abs_corr = abs(corr)

    if abs_corr > 0.9:
        strength = "Very strong"
    elif abs_corr > 0.7:
        strength = "Strong"
    elif abs_corr > 0.5:
        strength = "Moderate"
    elif abs_corr > 0.3:
        strength = "Weak"
    else:
        strength = "Very weak"

    direction = "positive" if corr > 0 else "negative"

    interpretations = {
        "very_strong_positive": "These stocks move very closely together",
        "strong_positive": "These stocks tend to move in the same direction",
        "moderate_positive": "These stocks show some tendency to move together",
        "weak_positive": "Minimal positive relationship",
        "very_weak_positive": "Almost no relationship",
        "very_weak_negative": "Almost no relationship",
        "weak_negative": "Minimal negative relationship",
        "moderate_negative": "These stocks show some tendency to move opposite",
        "strong_negative": "These stocks tend to move in opposite directions",
        "very_strong_negative": "These stocks move in strongly opposite directions"
    }

    key = f"{strength.lower().replace(' ', '_')}_{direction}"
    return interpretations.get(key, f"{strength} {direction} correlation")
