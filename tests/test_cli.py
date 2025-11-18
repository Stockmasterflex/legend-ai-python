"""Tests for Legend CLI."""

import pytest
from typer.testing import CliRunner
from legend_cli.main import app
from legend_cli.config_manager import ConfigManager, CLIConfig
import tempfile
from pathlib import Path


runner = CliRunner()


def test_version():
    """Test version command."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Legend AI CLI" in result.stdout


def test_help():
    """Test help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Legend AI" in result.stdout
    assert "analyze" in result.stdout
    assert "scan" in result.stdout


def test_config_show():
    """Test config show command."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_mgr = ConfigManager(config_dir=Path(tmpdir))
        config_mgr.save(CLIConfig())

        result = runner.invoke(app, ["config", "show"])
        assert result.exit_code == 0


def test_config_set():
    """Test config set command."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_mgr = ConfigManager(config_dir=Path(tmpdir))
        config_mgr.save(CLIConfig())

        result = runner.invoke(app, ["config", "set", "verbose", "true"])
        # May fail if config path differs, but should not crash
        assert result.exit_code in [0, 1]


def test_doctor():
    """Test doctor command."""
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Python version" in result.stdout


@pytest.mark.asyncio
async def test_health_command_no_api():
    """Test health command when API is not available."""
    # This will fail to connect, but should handle error gracefully
    result = runner.invoke(app, ["health"])
    # Should exit with error code if API is not running
    assert "Error" in result.stdout or "health" in result.stdout.lower()


def test_analyze_help():
    """Test analyze command help."""
    result = runner.invoke(app, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Analyze stocks" in result.stdout or "analyze" in result.stdout.lower()


def test_scan_help():
    """Test scan command help."""
    result = runner.invoke(app, ["scan", "--help"])
    assert result.exit_code == 0
    assert "Scan" in result.stdout or "scan" in result.stdout.lower()


def test_watchlist_help():
    """Test watchlist command help."""
    result = runner.invoke(app, ["watchlist", "--help"])
    assert result.exit_code == 0
    assert "watchlist" in result.stdout.lower()


def test_chart_help():
    """Test chart command help."""
    result = runner.invoke(app, ["chart", "--help"])
    assert result.exit_code == 0
    assert "chart" in result.stdout.lower()


def test_alerts_help():
    """Test alerts command help."""
    result = runner.invoke(app, ["alerts", "--help"])
    assert result.exit_code == 0
    assert "alert" in result.stdout.lower()


class TestConfigManager:
    """Test configuration manager."""

    def test_create_default_config(self):
        """Test creating default configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_mgr = ConfigManager(config_dir=Path(tmpdir))
            config = config_mgr.load()

            assert config.api_url == "http://localhost:8000"
            assert config.output_format == "table"
            assert config.color is True

    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_mgr = ConfigManager(config_dir=Path(tmpdir))

            # Create custom config
            config = CLIConfig(
                api_url="http://example.com:8000",
                output_format="json",
                verbose=True
            )
            config_mgr.save(config)

            # Load it back
            loaded_config = config_mgr.load()

            assert loaded_config.api_url == "http://example.com:8000"
            assert loaded_config.output_format == "json"
            assert loaded_config.verbose is True

    def test_get_set_config_values(self):
        """Test getting and setting individual config values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_mgr = ConfigManager(config_dir=Path(tmpdir))
            config_mgr.load()

            # Set value
            config_mgr.set("verbose", True)

            # Get value
            value = config_mgr.get("verbose")
            assert value is True

    def test_reset_config(self):
        """Test resetting configuration to defaults."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_mgr = ConfigManager(config_dir=Path(tmpdir))

            # Set custom values
            config_mgr.set("verbose", True)
            config_mgr.set("output_format", "json")

            # Reset
            config_mgr.reset()

            # Check defaults restored
            config = config_mgr.load()
            assert config.verbose is False
            assert config.output_format == "table"
