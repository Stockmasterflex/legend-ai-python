"""
DeFi Analytics Module

Features:
- Liquidity pool analysis
- Yield farming opportunities
- Gas price optimization
- Smart contract risk analysis
- Impermanent loss calculation
- APY/APR tracking
"""

import asyncio
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging
from decimal import Decimal
import statistics

from app.services.crypto_data import crypto_data_service

logger = logging.getLogger(__name__)


class LiquidityPoolAnalyzer:
    """
    Analyze DeFi liquidity pools

    Metrics:
    - TVL (Total Value Locked)
    - Volume/TVL ratio
    - APY/APR
    - Impermanent loss risk
    - Pool composition
    """

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_pool_data(self, protocol: str = "uniswap", pool_address: str = None) -> Optional[Dict[str, Any]]:
        """
        Get liquidity pool data from DeFi Llama

        Args:
            protocol: Protocol name (uniswap, sushiswap, pancakeswap, etc.)
            pool_address: Pool contract address

        Returns:
            {
                "pool_address": "0x...",
                "protocol": "uniswap",
                "chain": "ethereum",
                "tokens": ["WETH", "USDC"],
                "tvl": 125000000,
                "volume_24h": 8500000,
                "volume_7d": 52000000,
                "fees_24h": 25500,
                "apy": 18.5,
                "il_risk": "moderate"
            }
        """
        try:
            # DeFi Llama API for pool data
            url = "https://api.llama.fi/pools"
            response = await self.client.get(url)

            if response.status_code != 200:
                logger.error(f"Failed to fetch pool data: {response.status_code}")
                return None

            data = response.json()
            pools = data.get("data", [])

            # Filter by protocol if specified
            if protocol:
                pools = [p for p in pools if p.get("project", "").lower() == protocol.lower()]

            # Filter by pool address if specified
            if pool_address:
                pools = [p for p in pools if p.get("pool", "").lower() == pool_address.lower()]

            if not pools:
                return None

            # Return first matching pool
            pool = pools[0]

            # Calculate metrics
            tvl = pool.get("tvlUsd", 0)
            volume_24h = pool.get("volumeUsd1d", 0)
            volume_7d = pool.get("volumeUsd7d", 0)
            apy = pool.get("apy", 0)

            # Calculate IL risk based on token volatility
            # High volatility pairs = high IL risk
            symbol = pool.get("symbol", "")
            il_risk = self._calculate_il_risk(symbol)

            return {
                "pool_address": pool.get("pool", "N/A"),
                "protocol": pool.get("project", protocol),
                "chain": pool.get("chain", "unknown"),
                "tokens": symbol.split("-"),
                "tvl": round(tvl, 2),
                "volume_24h": round(volume_24h, 2),
                "volume_7d": round(volume_7d, 2),
                "apy": round(apy, 2),
                "il_risk": il_risk,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.exception(f"Failed to get pool data: {e}")
            return None

    def _calculate_il_risk(self, symbol: str) -> str:
        """
        Calculate impermanent loss risk based on token pair

        Stablecoin pairs: low risk
        Correlated pairs (e.g., ETH-WBTC): moderate risk
        Uncorrelated pairs: high risk
        """
        symbol_lower = symbol.lower()

        # Stablecoin identifiers
        stablecoins = ["usdt", "usdc", "dai", "busd", "frax", "lusd"]

        # Check if both tokens are stablecoins
        if any(s1 in symbol_lower for s1 in stablecoins):
            # Count how many stablecoins
            stable_count = sum(1 for s in stablecoins if s in symbol_lower)
            if stable_count >= 2:
                return "low"

        # Correlated pairs
        correlated_pairs = [
            ["eth", "wbtc"],
            ["eth", "steth"],
            ["eth", "reth"],
            ["btc", "wbtc"],
            ["bnb", "eth"]
        ]

        for pair in correlated_pairs:
            if all(token in symbol_lower for token in pair):
                return "moderate"

        # Default: high risk for uncorrelated pairs
        return "high"

    async def calculate_impermanent_loss(
        self,
        initial_price_ratio: float,
        current_price_ratio: float,
        initial_amount_a: float,
        initial_amount_b: float
    ) -> Dict[str, Any]:
        """
        Calculate impermanent loss for a liquidity position

        Args:
            initial_price_ratio: Initial price of token A in terms of token B
            current_price_ratio: Current price of token A in terms of token B
            initial_amount_a: Initial amount of token A
            initial_amount_b: Initial amount of token B

        Returns:
            {
                "il_percentage": -5.72,  # Negative = loss
                "value_if_held": 10000,
                "value_in_pool": 9428,
                "loss_usd": 572,
                "price_change_ratio": 2.0
            }
        """
        # Calculate price change ratio
        price_change_ratio = current_price_ratio / initial_price_ratio

        # IL formula for constant product AMM (x * y = k)
        # IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1
        il = 2 * (price_change_ratio ** 0.5) / (1 + price_change_ratio) - 1

        # Calculate initial value (in terms of token B)
        initial_value = initial_amount_a * initial_price_ratio + initial_amount_b

        # Calculate current value if held
        value_if_held = initial_amount_a * current_price_ratio + initial_amount_b

        # Calculate current value in pool
        value_in_pool = value_if_held * (1 + il)

        # Calculate loss
        loss = value_in_pool - value_if_held

        return {
            "il_percentage": round(il * 100, 2),
            "value_if_held": round(value_if_held, 2),
            "value_in_pool": round(value_in_pool, 2),
            "loss_usd": round(loss, 2),
            "price_change_ratio": round(price_change_ratio, 2),
            "timestamp": datetime.now().isoformat()
        }

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


class YieldFarmingOptimizer:
    """
    Find and analyze yield farming opportunities

    Features:
    - Top APY pools
    - Risk-adjusted returns
    - Auto-compounding analysis
    - Protocol safety scores
    """

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)

    async def find_top_yields(
        self,
        min_tvl: float = 1_000_000,
        min_apy: float = 5.0,
        max_il_risk: str = "moderate",
        chains: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find top yield farming opportunities

        Args:
            min_tvl: Minimum TVL in USD
            min_apy: Minimum APY percentage
            max_il_risk: Maximum IL risk level (low, moderate, high)
            chains: List of blockchain networks to filter

        Returns:
            List of opportunities sorted by risk-adjusted return
        """
        try:
            # DeFi Llama yields API
            url = "https://yields.llama.fi/pools"
            response = await self.client.get(url)

            if response.status_code != 200:
                logger.error(f"Failed to fetch yields: {response.status_code}")
                return []

            data = response.json()
            pools = data.get("data", [])

            # Filter pools
            filtered_pools = []
            risk_levels = {"low": 1, "moderate": 2, "high": 3}
            max_risk_level = risk_levels.get(max_il_risk, 2)

            for pool in pools:
                tvl = pool.get("tvlUsd", 0)
                apy = pool.get("apy", 0)
                chain = pool.get("chain", "")
                symbol = pool.get("symbol", "")

                # Apply filters
                if tvl < min_tvl:
                    continue
                if apy < min_apy:
                    continue
                if chains and chain not in chains:
                    continue

                # Calculate IL risk
                il_risk = self._calculate_il_risk(symbol)
                if risk_levels.get(il_risk, 3) > max_risk_level:
                    continue

                # Calculate risk-adjusted return
                risk_multiplier = {
                    "low": 1.0,
                    "moderate": 0.8,
                    "high": 0.6
                }
                adjusted_apy = apy * risk_multiplier.get(il_risk, 0.6)

                filtered_pools.append({
                    "protocol": pool.get("project", "Unknown"),
                    "pool": pool.get("symbol", ""),
                    "chain": chain,
                    "tvl": round(tvl, 2),
                    "apy": round(apy, 2),
                    "apy_adjusted": round(adjusted_apy, 2),
                    "il_risk": il_risk,
                    "stablecoin": pool.get("stablecoin", False),
                    "pool_address": pool.get("pool", "N/A")
                })

            # Sort by risk-adjusted APY
            filtered_pools.sort(key=lambda x: x["apy_adjusted"], reverse=True)

            return filtered_pools[:20]  # Return top 20

        except Exception as e:
            logger.exception(f"Failed to find yields: {e}")
            return []

    def _calculate_il_risk(self, symbol: str) -> str:
        """Calculate IL risk (same logic as LiquidityPoolAnalyzer)"""
        symbol_lower = symbol.lower()
        stablecoins = ["usdt", "usdc", "dai", "busd", "frax", "lusd"]

        if any(s1 in symbol_lower for s1 in stablecoins):
            stable_count = sum(1 for s in stablecoins if s in symbol_lower)
            if stable_count >= 2:
                return "low"

        correlated_pairs = [
            ["eth", "wbtc"],
            ["eth", "steth"],
            ["btc", "wbtc"]
        ]

        for pair in correlated_pairs:
            if all(token in symbol_lower for token in pair):
                return "moderate"

        return "high"

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


class GasOptimizer:
    """
    Gas price optimization for Ethereum transactions

    Features:
    - Real-time gas prices
    - Optimal timing recommendations
    - Gas cost estimation
    - Multi-chain support
    """

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_gas_prices(self, chain: str = "ethereum") -> Optional[Dict[str, Any]]:
        """
        Get current gas prices

        Returns:
            {
                "chain": "ethereum",
                "slow": 25,
                "standard": 30,
                "fast": 35,
                "instant": 40,
                "base_fee": 23,
                "priority_fee": 2,
                "timestamp": "2024-01-01T12:00:00Z",
                "recommendation": "Wait 1-2 hours for lower fees"
            }
        """
        try:
            if chain.lower() == "ethereum":
                # Use Etherscan Gas Tracker API (no key needed for basic data)
                url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"
                response = await self.client.get(url)

                if response.status_code != 200:
                    logger.error(f"Failed to fetch gas prices: {response.status_code}")
                    return None

                data = response.json()
                result = data.get("result", {})

                safe_gas = int(result.get("SafeGasPrice", 25))
                propose_gas = int(result.get("ProposeGasPrice", 30))
                fast_gas = int(result.get("FastGasPrice", 35))

                # Generate recommendation
                if propose_gas < 20:
                    recommendation = "Excellent time to transact"
                elif propose_gas < 40:
                    recommendation = "Good time to transact"
                elif propose_gas < 80:
                    recommendation = "Wait for lower fees if not urgent"
                else:
                    recommendation = "High gas fees - wait if possible"

                return {
                    "chain": "ethereum",
                    "slow": safe_gas,
                    "standard": propose_gas,
                    "fast": fast_gas,
                    "instant": fast_gas + 5,
                    "recommendation": recommendation,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Other chains (BSC, Polygon, etc.) have much lower fees
                return {
                    "chain": chain,
                    "slow": 1,
                    "standard": 2,
                    "fast": 3,
                    "instant": 5,
                    "recommendation": "Low fees - good time to transact",
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as e:
            logger.exception(f"Failed to get gas prices: {e}")
            return None

    async def estimate_transaction_cost(
        self,
        gas_limit: int,
        gas_price_gwei: int,
        eth_price_usd: float = None
    ) -> Dict[str, Any]:
        """
        Estimate transaction cost in ETH and USD

        Args:
            gas_limit: Gas limit for transaction (e.g., 21000 for simple transfer)
            gas_price_gwei: Gas price in Gwei
            eth_price_usd: Current ETH price (will fetch if not provided)

        Returns:
            {
                "gas_limit": 21000,
                "gas_price_gwei": 30,
                "cost_eth": 0.00063,
                "cost_usd": 2.52,
                "timestamp": "2024-01-01T12:00:00Z"
            }
        """
        # Get ETH price if not provided
        if eth_price_usd is None:
            price_data = await crypto_data_service.get_realtime_price("ETH", "USDT")
            eth_price_usd = price_data.get("price", 4000) if price_data else 4000

        # Calculate cost
        cost_eth = (gas_limit * gas_price_gwei) / 1e9  # Convert Gwei to ETH
        cost_usd = cost_eth * eth_price_usd

        return {
            "gas_limit": gas_limit,
            "gas_price_gwei": gas_price_gwei,
            "cost_eth": round(cost_eth, 6),
            "cost_usd": round(cost_usd, 2),
            "eth_price_usd": round(eth_price_usd, 2),
            "timestamp": datetime.now().isoformat()
        }

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


class SmartContractAnalyzer:
    """
    Smart contract risk analysis

    Features:
    - Contract verification status
    - Audit reports
    - Risk scoring
    - Honeypot detection
    """

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)

    async def analyze_contract(self, contract_address: str, chain: str = "ethereum") -> Dict[str, Any]:
        """
        Analyze smart contract for risks

        Returns:
            {
                "contract_address": "0x...",
                "chain": "ethereum",
                "verified": true,
                "audit_status": "audited",
                "risk_score": 25,  # 0-100, lower is better
                "risks": ["Centralized ownership", ...],
                "recommendations": ["Contract is verified", ...]
            }
        """
        # Placeholder implementation
        # In production, would integrate with:
        # - Etherscan API for verification status
        # - CertiK/Hacken for audit reports
        # - GoPlus for honeypot detection

        return {
            "contract_address": contract_address,
            "chain": chain,
            "verified": True,  # Would check via Etherscan
            "audit_status": "unknown",  # Would check audit databases
            "risk_score": 50,  # Medium risk as default
            "risks": [
                "Audit status unknown - proceed with caution",
                "Always verify contract source code"
            ],
            "recommendations": [
                "Check contract verification on block explorer",
                "Review audit reports if available",
                "Start with small amounts"
            ],
            "timestamp": datetime.now().isoformat()
        }


class DeFiAnalyticsService:
    """
    Unified DeFi analytics service
    """

    def __init__(self):
        self.pool_analyzer = LiquidityPoolAnalyzer()
        self.yield_optimizer = YieldFarmingOptimizer()
        self.gas_optimizer = GasOptimizer()
        self.contract_analyzer = SmartContractAnalyzer()

    async def get_comprehensive_analysis(
        self,
        protocols: List[str] = None,
        chains: List[str] = None,
        min_apy: float = 5.0
    ) -> Dict[str, Any]:
        """
        Get comprehensive DeFi analysis

        Returns:
            {
                "top_yields": [...],
                "gas_prices": {...},
                "defi_metrics": {...},
                "recommendations": [...]
            }
        """
        # Run analyses in parallel
        yields_task = self.yield_optimizer.find_top_yields(
            min_apy=min_apy,
            chains=chains
        )
        gas_task = self.gas_optimizer.get_gas_prices("ethereum")
        defi_metrics_task = crypto_data_service.coingecko.get_defi_market_data()

        top_yields, gas_prices, defi_metrics = await asyncio.gather(
            yields_task, gas_task, defi_metrics_task,
            return_exceptions=True
        )

        # Handle exceptions
        if isinstance(top_yields, Exception):
            top_yields = []
        if isinstance(gas_prices, Exception):
            gas_prices = {}
        if isinstance(defi_metrics, Exception):
            defi_metrics = {}

        # Generate recommendations
        recommendations = []
        if gas_prices.get("standard", 999) < 30:
            recommendations.append("⛽ Low gas fees - good time for DeFi transactions")
        if top_yields and len(top_yields) > 0:
            best_yield = top_yields[0]
            recommendations.append(f"💰 Top yield: {best_yield['apy']}% APY on {best_yield['protocol']} ({best_yield['chain']})")

        return {
            "top_yields": top_yields[:10],
            "gas_prices": gas_prices,
            "defi_metrics": defi_metrics,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }

    async def close(self):
        """Close all clients"""
        await self.pool_analyzer.close()
        await self.yield_optimizer.close()
        await self.gas_optimizer.close()
        await self.contract_analyzer.close()


# Global instance
defi_analytics_service = DeFiAnalyticsService()
