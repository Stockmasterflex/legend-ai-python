#!/usr/bin/env python3
"""Quick verification script for Legend CLI."""

import sys
import importlib.util


def check_import(module_name):
    """Check if a module can be imported."""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"✓ {module_name}")
            return True
        else:
            print(f"✗ {module_name} (not found)")
            return False
    except Exception as e:
        print(f"✗ {module_name} (error: {e})")
        return False


def main():
    """Run verification checks."""
    print("Legend AI CLI - Verification\n")

    print("Checking imports:")
    checks = [
        "legend_cli",
        "legend_cli.main",
        "legend_cli.client",
        "legend_cli.config_manager",
        "legend_cli.formatters",
        "legend_cli.utils",
        "legend_cli.commands.analyze",
        "legend_cli.commands.scan",
        "legend_cli.commands.watchlist",
        "legend_cli.commands.chart",
        "legend_cli.commands.alerts",
        "legend_cli.commands.config",
    ]

    passed = sum(check_import(module) for module in checks)
    total = len(checks)

    print(f"\nResults: {passed}/{total} checks passed")

    if passed == total:
        print("\n✓ All CLI modules verified!")
        return 0
    else:
        print(f"\n✗ {total - passed} checks failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
