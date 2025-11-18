"""
Detector Registry - Central registry for all pattern detectors

This module provides a central registry for all available pattern detectors,
making it easy to discover, instantiate, and use detectors throughout the application.
"""
from typing import Dict, List, Type, Optional
import logging

from app.core.detector_base import Detector, PatternResult
from app.core.detectors.vcp_detector import VCPDetector
from app.core.detectors.cup_handle_detector import CupHandleDetector
from app.core.detectors.triangle_detector import TriangleDetector
from app.core.detectors.wedge_detector import WedgeDetector
from app.core.detectors.head_shoulders_detector import HeadShouldersDetector
from app.core.detectors.double_top_bottom_detector import DoubleTopBottomDetector
from app.core.detectors.channel_detector import ChannelDetector
from app.core.detectors.sma50_pullback_detector import SMA50PullbackDetector

logger = logging.getLogger(__name__)


class DetectorRegistry:
    """
    Registry for all available pattern detectors

    Provides centralized access to all detector classes and their capabilities.
    """

    def __init__(self):
        """Initialize the detector registry with all available detectors"""
        self._detectors: Dict[str, Type[Detector]] = {}
        self._pattern_to_detector: Dict[str, str] = {}

        # Register all detectors
        self._register_all()

    def _register_all(self) -> None:
        """Register all available detectors"""
        # Register each detector
        self.register("vcp", VCPDetector, ["VCP", "Volatility Contraction Pattern"])
        self.register("cup_handle", CupHandleDetector, ["Cup & Handle", "Cup with Handle"])
        self.register("triangle", TriangleDetector, [
            "Ascending Triangle",
            "Descending Triangle",
            "Symmetrical Triangle"
        ])
        self.register("wedge", WedgeDetector, ["Rising Wedge", "Falling Wedge"])
        self.register("head_shoulders", HeadShouldersDetector, [
            "Head & Shoulders",
            "Inverse Head & Shoulders"
        ])
        self.register("double_pattern", DoubleTopBottomDetector, [
            "Double Top",
            "Double Bottom"
        ])
        self.register("channel", ChannelDetector, [
            "Channel Up",
            "Channel Down",
            "Sideways Channel"
        ])
        self.register("sma50_pullback", SMA50PullbackDetector, ["50 SMA Pullback"])

        logger.info(f"✅ Registered {len(self._detectors)} pattern detectors")

    def register(
        self,
        detector_id: str,
        detector_class: Type[Detector],
        pattern_names: List[str]
    ) -> None:
        """
        Register a detector

        Args:
            detector_id: Unique identifier for the detector
            detector_class: The detector class (subclass of Detector)
            pattern_names: List of pattern names this detector can identify
        """
        self._detectors[detector_id] = detector_class

        # Map each pattern name to this detector
        for pattern_name in pattern_names:
            self._pattern_to_detector[pattern_name.lower()] = detector_id

    def get_detector(self, detector_id: str, **kwargs) -> Optional[Detector]:
        """
        Get an instance of a detector by ID

        Args:
            detector_id: The detector ID
            **kwargs: Arguments to pass to detector constructor

        Returns:
            Instantiated detector or None if not found
        """
        detector_class = self._detectors.get(detector_id)
        if not detector_class:
            logger.warning(f"Detector '{detector_id}' not found in registry")
            return None

        try:
            return detector_class(**kwargs)
        except Exception as e:
            logger.error(f"Failed to instantiate detector '{detector_id}': {e}")
            return None

    def get_detector_for_pattern(self, pattern_name: str, **kwargs) -> Optional[Detector]:
        """
        Get a detector that can detect the specified pattern

        Args:
            pattern_name: Name of the pattern to detect
            **kwargs: Arguments to pass to detector constructor

        Returns:
            Instantiated detector or None if not found
        """
        detector_id = self._pattern_to_detector.get(pattern_name.lower())
        if not detector_id:
            logger.warning(f"No detector found for pattern '{pattern_name}'")
            return None

        return self.get_detector(detector_id, **kwargs)

    def get_all_detectors(self, **kwargs) -> List[Detector]:
        """
        Get instances of all registered detectors

        Args:
            **kwargs: Arguments to pass to detector constructors

        Returns:
            List of instantiated detectors
        """
        detectors = []
        for detector_id in self._detectors.keys():
            detector = self.get_detector(detector_id, **kwargs)
            if detector:
                detectors.append(detector)
        return detectors

    def list_detector_ids(self) -> List[str]:
        """Get list of all registered detector IDs"""
        return list(self._detectors.keys())

    def list_all_patterns(self) -> List[str]:
        """Get list of all pattern names that can be detected"""
        return list(self._pattern_to_detector.keys())


# Global registry instance
_registry: Optional[DetectorRegistry] = None


def get_detector_registry() -> DetectorRegistry:
    """
    Get the global detector registry instance (singleton)

    Returns:
        The detector registry
    """
    global _registry
    if _registry is None:
        _registry = DetectorRegistry()
    return _registry


# Convenience functions
def get_detector(detector_id: str, **kwargs) -> Optional[Detector]:
    """Get a detector by ID"""
    return get_detector_registry().get_detector(detector_id, **kwargs)


def get_detector_for_pattern(pattern_name: str, **kwargs) -> Optional[Detector]:
    """Get a detector for a specific pattern"""
    return get_detector_registry().get_detector_for_pattern(pattern_name, **kwargs)


def get_all_detectors(**kwargs) -> List[Detector]:
    """Get all available detectors"""
    return get_detector_registry().get_all_detectors(**kwargs)


def list_all_patterns() -> List[str]:
    """List all detectable patterns"""
    return get_detector_registry().list_all_patterns()
