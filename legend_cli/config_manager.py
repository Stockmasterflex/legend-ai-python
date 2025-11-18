"""Configuration management for Legend CLI."""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml
from pydantic import BaseModel, Field, validator


class CLIConfig(BaseModel):
    """CLI configuration model."""

    # API Configuration
    api_url: str = Field(default="http://localhost:8000", description="Legend AI API URL")
    api_key: Optional[str] = Field(default=None, description="API key for authentication")
    timeout: int = Field(default=30, description="API request timeout in seconds")

    # Output Configuration
    output_format: str = Field(default="table", description="Default output format (table, json, csv)")
    color: bool = Field(default=True, description="Enable colored output")
    verbose: bool = Field(default=False, description="Enable verbose output")

    # TUI Configuration
    tui_refresh_interval: int = Field(default=5, description="TUI refresh interval in seconds")
    tui_theme: str = Field(default="dark", description="TUI theme (dark, light)")

    # Cache Configuration
    cache_enabled: bool = Field(default=True, description="Enable local caching")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")

    # Watchlist Configuration
    default_watchlist: str = Field(default="default", description="Default watchlist name")

    @validator('output_format')
    def validate_output_format(cls, v):
        """Validate output format."""
        valid_formats = ['table', 'json', 'csv', 'yaml']
        if v not in valid_formats:
            raise ValueError(f"Invalid output format. Must be one of: {', '.join(valid_formats)}")
        return v

    @validator('tui_theme')
    def validate_theme(cls, v):
        """Validate TUI theme."""
        valid_themes = ['dark', 'light']
        if v not in valid_themes:
            raise ValueError(f"Invalid theme. Must be one of: {', '.join(valid_themes)}")
        return v


class ConfigManager:
    """Manages CLI configuration."""

    DEFAULT_CONFIG_DIR = Path.home() / ".legend"
    DEFAULT_CONFIG_FILE = "config.yaml"

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize config manager."""
        self.config_dir = config_dir or self.DEFAULT_CONFIG_DIR
        self.config_file = self.config_dir / self.DEFAULT_CONFIG_FILE
        self._config: Optional[CLIConfig] = None

        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> CLIConfig:
        """Load configuration from file."""
        if self._config is not None:
            return self._config

        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                data = yaml.safe_load(f) or {}
                self._config = CLIConfig(**data)
        else:
            # Create default config
            self._config = CLIConfig()
            self.save(self._config)

        # Override with environment variables
        self._apply_env_overrides()

        return self._config

    def _apply_env_overrides(self):
        """Apply environment variable overrides."""
        if not self._config:
            return

        # Override API URL from environment
        if url := os.getenv("LEGEND_API_URL"):
            self._config.api_url = url

        # Override API key from environment
        if key := os.getenv("LEGEND_API_KEY"):
            self._config.api_key = key

        # Override output format
        if fmt := os.getenv("LEGEND_OUTPUT_FORMAT"):
            self._config.output_format = fmt

    def save(self, config: CLIConfig):
        """Save configuration to file."""
        self._config = config

        with open(self.config_file, 'w') as f:
            # Convert to dict and remove None values
            config_dict = config.model_dump(exclude_none=True)
            yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        config = self.load()
        return getattr(config, key, default)

    def set(self, key: str, value: Any):
        """Set configuration value."""
        config = self.load()
        setattr(config, key, value)
        self.save(config)

    def reset(self):
        """Reset configuration to defaults."""
        self._config = CLIConfig()
        self.save(self._config)

    def show(self) -> Dict[str, Any]:
        """Show current configuration."""
        config = self.load()
        return config.model_dump()


# Global config manager instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get global config manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_config() -> CLIConfig:
    """Get current configuration."""
    return get_config_manager().load()
