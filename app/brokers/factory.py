"""
Broker Factory

Factory pattern for creating broker instances based on broker type.
"""

from typing import Dict, Optional
import logging

from app.brokers.base import BaseBroker, BrokerType
from app.brokers.alpaca import AlpacaBroker
from app.brokers.td_ameritrade import TDAmeritradeBroker
from app.brokers.interactive_brokers import InteractiveBrokersBroker
from app.brokers.tradestation import TradeStationBroker

logger = logging.getLogger(__name__)


class BrokerFactory:
    """
    Factory for creating broker instances.

    Usage:
        broker = BrokerFactory.create(
            BrokerType.ALPACA,
            credentials={"api_key": "...", "api_secret": "..."},
            paper_trading=True
        )
        async with broker:
            account = await broker.get_account()
            positions = await broker.get_positions()
    """

    _broker_classes = {
        BrokerType.ALPACA: AlpacaBroker,
        BrokerType.TD_AMERITRADE: TDAmeritradeBroker,
        BrokerType.INTERACTIVE_BROKERS: InteractiveBrokersBroker,
        BrokerType.TRADESTATION: TradeStationBroker,
    }

    @classmethod
    def create(
        cls,
        broker_type: BrokerType,
        credentials: Dict[str, str],
        paper_trading: bool = True,
    ) -> BaseBroker:
        """
        Create a broker instance.

        Args:
            broker_type: Type of broker to create
            credentials: API credentials for the broker
            paper_trading: Whether to use paper/simulation trading (default: True)

        Returns:
            BaseBroker: Configured broker instance

        Raises:
            ValueError: If broker type is not supported
        """
        if broker_type not in cls._broker_classes:
            raise ValueError(
                f"Unsupported broker type: {broker_type}. "
                f"Supported types: {', '.join([b.value for b in cls._broker_classes.keys()])}"
            )

        broker_class = cls._broker_classes[broker_type]
        broker = broker_class(credentials=credentials, paper_trading=paper_trading)

        logger.info(f"Created {broker_type.value} broker instance (paper_trading={paper_trading})")
        return broker

    @classmethod
    def create_from_config(
        cls,
        broker_type: BrokerType,
        config: Dict[str, any],
    ) -> BaseBroker:
        """
        Create a broker instance from configuration dict.

        Args:
            broker_type: Type of broker to create
            config: Configuration dict with 'credentials' and optional 'paper_trading'

        Returns:
            BaseBroker: Configured broker instance

        Example:
            config = {
                "credentials": {
                    "api_key": "...",
                    "api_secret": "..."
                },
                "paper_trading": True
            }
            broker = BrokerFactory.create_from_config(BrokerType.ALPACA, config)
        """
        credentials = config.get("credentials", {})
        paper_trading = config.get("paper_trading", True)

        return cls.create(
            broker_type=broker_type,
            credentials=credentials,
            paper_trading=paper_trading,
        )

    @classmethod
    def supported_brokers(cls) -> list[BrokerType]:
        """
        Get list of supported broker types.

        Returns:
            list[BrokerType]: List of supported brokers
        """
        return list(cls._broker_classes.keys())

    @classmethod
    def get_required_credentials(cls, broker_type: BrokerType) -> Dict[str, str]:
        """
        Get required credential fields for a broker type.

        Args:
            broker_type: Type of broker

        Returns:
            Dict[str, str]: Dictionary of required credential fields and their descriptions
        """
        credentials_map = {
            BrokerType.ALPACA: {
                "api_key": "Alpaca API Key ID",
                "api_secret": "Alpaca API Secret Key",
            },
            BrokerType.TD_AMERITRADE: {
                "api_key": "TD Ameritrade Consumer Key (API Key)",
                "refresh_token": "OAuth Refresh Token",
                "account_id": "Account ID",
            },
            BrokerType.INTERACTIVE_BROKERS: {
                "gateway_url": "Client Portal Gateway URL (optional, defaults to localhost:5000)",
                "account_id": "Account ID (optional, will be auto-detected)",
            },
            BrokerType.TRADESTATION: {
                "api_key": "TradeStation API Key (Client ID)",
                "api_secret": "TradeStation API Secret",
                "refresh_token": "OAuth Refresh Token",
                "account_id": "Account ID (optional)",
            },
        }

        return credentials_map.get(broker_type, {})
