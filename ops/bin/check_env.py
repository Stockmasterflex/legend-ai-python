#!/usr/bin/env python3
"""
Verify required telemetry-related environment variables are present.
Outputs booleans only to avoid leaking secrets.
"""

from __future__ import annotations

import os
import sys
from typing import List

REQUIRED_ENV_VARS: List[str] = [
    "TELEGRAM_BOT_TOKEN",
    "OPENROUTER_API_KEY",
    "CHARTIMG_API_KEY",
    "TWELVEDATA_API_KEY",
    "FINNHUB_API_KEY",
    "ALPHA_VANTAGE_API_KEY",
    "REDIS_URL",
]


def main() -> int:
    missing = []
    for name in REQUIRED_ENV_VARS:
        present = bool(os.getenv(name))
        print(f"{name}={'true' if present else 'false'}")
        if not present:
            missing.append(name)

    passed = not missing
    print(f"env_check_passed={'true' if passed else 'false'}")

    if not passed:
        sys.stderr.write(
            "Missing required environment variables: "
            + ", ".join(missing)
            + "\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
