#!/usr/bin/env python3
"""
Verify required telemetry-related environment variables are present.
Outputs booleans only to avoid leaking secrets.

In CI test mode (--ci-mode), missing API keys are warnings, not failures.
This allows unit tests to run without production secrets.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List

# Required for production deployment
REQUIRED_ENV_VARS: List[str] = [
    "TELEGRAM_BOT_TOKEN",
    "OPENROUTER_API_KEY",
    "CHARTIMG_API_KEY",
    "TWELVEDATA_API_KEY",
    "FINNHUB_API_KEY",
    "ALPHA_VANTAGE_API_KEY",
    "REDIS_URL",
]

# Required even in CI test mode
CRITICAL_ENV_VARS: List[str] = [
    "REDIS_URL",  # Needed for test suite
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check environment variables")
    parser.add_argument(
        "--ci-mode",
        action="store_true",
        help="CI test mode: missing API keys are warnings, not failures",
    )
    args = parser.parse_args()

    missing = []
    critical_missing = []

    for name in REQUIRED_ENV_VARS:
        present = bool(os.getenv(name))
        print(f"{name}={'true' if present else 'false'}")
        if not present:
            missing.append(name)
            if name in CRITICAL_ENV_VARS:
                critical_missing.append(name)

    # In CI mode, only fail if critical vars are missing
    if args.ci_mode:
        if critical_missing:
            print(f"env_check_passed=false")
            sys.stderr.write(
                "❌ CI Mode: Missing critical environment variables: "
                + ", ".join(critical_missing)
                + "\n"
            )
            return 1
        elif missing:
            print(f"env_check_passed=true")
            print(
                f"⚠️  CI Mode: Missing optional API keys (OK for tests): "
                + ", ".join(missing)
            )
            return 0
        else:
            print(f"env_check_passed=true")
            return 0

    # Production mode: require all vars
    passed = not missing
    print(f"env_check_passed={'true' if passed else 'false'}")

    if not passed:
        sys.stderr.write(
            "❌ Production Mode: Missing required environment variables: "
            + ", ".join(missing)
            + "\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
