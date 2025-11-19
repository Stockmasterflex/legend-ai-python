#!/usr/bin/env python3
"""
Environment Variable Validation Script
Checks that all required environment variables are set
"""

import os
import sys
from typing import List, Tuple

# Color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

# Required environment variables (critical for app to function)
REQUIRED_VARS = [
    "SECRET_KEY",
    "DATABASE_URL",
]

# Recommended environment variables (app can run but with degraded functionality)
RECOMMENDED_VARS = [
    "REDIS_URL",
    "TELEGRAM_BOT_TOKEN",
    "TWELVEDATA_API_KEY",
    "CHART_IMG_API_KEY",
    "OPENROUTER_API_KEY",
]

# Optional but useful
OPTIONAL_VARS = [
    "TELEGRAM_CHAT_ID",
    "FINNHUB_API_KEY",
    "ALPHA_VANTAGE_API_KEY",
    "OPENAI_API_KEY",
    "DEBUG",
    "LOG_LEVEL",
]


def check_env_var(var_name: str) -> Tuple[bool, str]:
    """Check if environment variable is set and return its status"""
    value = os.getenv(var_name)

    if value is None or value == "":
        return False, f"{RED}✗ {var_name} - NOT SET{NC}"

    # Mask sensitive values
    if len(value) > 20:
        display_value = value[:8] + "..." + value[-4:]
    else:
        display_value = value[:4] + "..."

    return True, f"{GREEN}✓ {var_name} - {display_value}{NC}"


def main():
    print(f"{BLUE}Checking environment variables...{NC}\n")

    all_passed = True
    warnings = []

    # Check required variables
    print(f"{BLUE}Required Variables:{NC}")
    for var in REQUIRED_VARS:
        is_set, message = check_env_var(var)
        print(f"  {message}")
        if not is_set:
            all_passed = False

    print()

    # Check recommended variables
    print(f"{BLUE}Recommended Variables:{NC}")
    for var in RECOMMENDED_VARS:
        is_set, message = check_env_var(var)
        print(f"  {message}")
        if not is_set:
            warnings.append(var)

    print()

    # Check optional variables
    print(f"{BLUE}Optional Variables:{NC}")
    for var in OPTIONAL_VARS:
        is_set, message = check_env_var(var)
        print(f"  {message}")

    print()

    # Summary
    if not all_passed:
        print(f"{RED}❌ CRITICAL: Required environment variables are missing!{NC}")
        print(f"{RED}Deployment cannot proceed.{NC}")
        return 1

    if warnings:
        print(f"{YELLOW}⚠ WARNING: Some recommended variables are not set:{NC}")
        for var in warnings:
            print(f"  - {var}")
        print(f"{YELLOW}Application may have degraded functionality.{NC}")
        print()

    print(f"{GREEN}✓ Environment validation passed!{NC}")

    # Additional checks
    print(f"\n{BLUE}Additional Checks:{NC}")

    # Check Railway environment
    if os.getenv("RAILWAY_ENVIRONMENT"):
        print(f"  {GREEN}✓ Railway environment detected{NC}")
        if os.getenv("RAILWAY_PUBLIC_DOMAIN"):
            print(f"  {GREEN}✓ Railway public domain: {os.getenv('RAILWAY_PUBLIC_DOMAIN')}{NC}")

    # Check if DATABASE_URL is PostgreSQL
    db_url = os.getenv("DATABASE_URL", "")
    if "postgresql" in db_url or "postgres" in db_url:
        print(f"  {GREEN}✓ PostgreSQL database configured{NC}")
    elif db_url:
        print(f"  {YELLOW}⚠ Non-PostgreSQL database detected{NC}")

    # Check Redis URL
    redis_url = os.getenv("REDIS_URL", "")
    if "redis" in redis_url:
        print(f"  {GREEN}✓ Redis configured{NC}")
    elif not redis_url:
        print(f"  {YELLOW}⚠ Redis not configured (caching disabled){NC}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
