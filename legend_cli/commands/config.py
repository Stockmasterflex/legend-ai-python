"""Config command for Legend CLI."""

import typer
from rich.console import Console
from rich.table import Table
from rich import box

from ..config_manager import get_config_manager, CLIConfig
from ..formatters import OutputFormatter

app = typer.Typer(help="Manage CLI configuration")
console = Console()
formatter = OutputFormatter(console)


@app.command()
def show(
    output: str = typer.Option("table", "--output", "-o", help="Output format (table/json/yaml)")
):
    """Show current configuration."""
    try:
        config_mgr = get_config_manager()
        config = config_mgr.show()

        if output == "json":
            console.print(formatter.format_json(config))
        elif output == "yaml":
            console.print(formatter.format_yaml(config))
        else:
            # Table format
            table = Table(
                title="Legend CLI Configuration",
                box=box.ROUNDED,
                show_header=True,
                header_style="bold cyan"
            )

            table.add_column("Setting", style="cyan", no_wrap=True)
            table.add_column("Value", style="white")

            for key, value in config.items():
                # Mask API key for security
                if 'key' in key.lower() and value:
                    value = f"{value[:8]}..." if len(value) > 8 else "***"
                table.add_row(key, str(value))

            console.print(table)

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
def set(
    key: str = typer.Argument(..., help="Configuration key"),
    value: str = typer.Argument(..., help="Configuration value")
):
    """Set a configuration value."""
    try:
        config_mgr = get_config_manager()

        # Validate key exists in model
        try:
            config = config_mgr.load()
            if not hasattr(config, key):
                formatter.print_error(f"Invalid configuration key: {key}")
                formatter.print_info("Use 'legend config show' to see available keys")
                raise typer.Exit(1)

            # Convert value to appropriate type
            field_type = type(getattr(config, key))

            if field_type == bool:
                value = value.lower() in ('true', '1', 'yes', 'on')
            elif field_type == int:
                value = int(value)
            elif field_type == float:
                value = float(value)

            # Set value
            config_mgr.set(key, value)
            formatter.print_success(f"Set {key} = {value}")

        except ValueError as e:
            formatter.print_error(f"Invalid value for {key}: {e}")
            raise typer.Exit(1)

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
def reset():
    """Reset configuration to defaults."""
    try:
        if not typer.confirm("Reset configuration to defaults?"):
            formatter.print_info("Cancelled")
            return

        config_mgr = get_config_manager()
        config_mgr.reset()

        formatter.print_success("Configuration reset to defaults")

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
def path():
    """Show configuration file path."""
    try:
        config_mgr = get_config_manager()
        console.print(f"[cyan]Config directory:[/cyan] {config_mgr.config_dir}")
        console.print(f"[cyan]Config file:[/cyan] {config_mgr.config_file}")

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
def init(
    api_url: str = typer.Option("http://localhost:8000", "--api-url", help="API URL"),
    api_key: str = typer.Option(None, "--api-key", help="API key"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing config")
):
    """Initialize configuration interactively."""
    try:
        config_mgr = get_config_manager()

        # Check if config exists
        if config_mgr.config_file.exists() and not force:
            if not typer.confirm("Configuration already exists. Overwrite?"):
                formatter.print_info("Cancelled")
                return

        # Create new config
        config = CLIConfig(
            api_url=api_url,
            api_key=api_key
        )

        # Interactive prompts for additional settings
        if typer.confirm("Configure output format?", default=False):
            fmt = typer.prompt(
                "Output format",
                default="table",
                type=typer.Choice(['table', 'json', 'csv', 'yaml'])
            )
            config.output_format = fmt

        if typer.confirm("Configure colors?", default=False):
            config.color = typer.confirm("Enable colored output?", default=True)

        # Save config
        config_mgr.save(config)

        formatter.print_success(f"Configuration initialized at {config_mgr.config_file}")
        formatter.print_info("Use 'legend config show' to view settings")

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)
