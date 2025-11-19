#!/usr/bin/env python3
"""
Backup Monitoring Script
Checks backup status and sends alerts if backups are missing or old
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import requests

SCRIPT_DIR = Path(__file__).parent
BACKUP_DIRS = {
    "database": SCRIPT_DIR / "backups" / "database",
    "universe": SCRIPT_DIR / "backups" / "universe",
    "redis": SCRIPT_DIR / "backups" / "redis",
}

# Alert thresholds (hours)
THRESHOLDS = {
    "database": 24,  # Alert if no backup in 24 hours
    "universe": 168,  # Alert if no backup in 7 days
    "redis": 24,  # Alert if no backup in 24 hours
}


def send_telegram(message: str):
    """Send Telegram notification"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print(f"Failed to send Telegram: {e}")


def check_backups():
    """Check all backup directories"""
    alerts = []
    status = {}

    for backup_type, backup_dir in BACKUP_DIRS.items():
        if not backup_dir.exists():
            alerts.append(f"❌ {backup_type}: Directory missing!")
            status[backup_type] = {
                "status": "missing",
                "latest": None,
                "age_hours": None
            }
            continue

        # Find latest backup
        files = list(backup_dir.glob("*"))
        if not files:
            alerts.append(f"⚠️ {backup_type}: No backups found!")
            status[backup_type] = {
                "status": "no_backups",
                "latest": None,
                "age_hours": None
            }
            continue

        # Get latest file
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        latest_time = datetime.fromtimestamp(latest_file.stat().st_mtime)
        age = datetime.now() - latest_time
        age_hours = age.total_seconds() / 3600

        status[backup_type] = {
            "status": "ok" if age_hours < THRESHOLDS[backup_type] else "old",
            "latest": str(latest_file.name),
            "age_hours": age_hours,
            "threshold_hours": THRESHOLDS[backup_type]
        }

        # Check if backup is too old
        if age_hours > THRESHOLDS[backup_type]:
            alerts.append(
                f"⚠️ {backup_type}: Latest backup is {age_hours:.1f} hours old "
                f"(threshold: {THRESHOLDS[backup_type]} hours)"
            )
        else:
            print(f"✅ {backup_type}: OK ({age_hours:.1f} hours old)")

    return status, alerts


def main():
    """Main entry point"""
    print("=" * 60)
    print(f"Backup Monitoring - {datetime.now()}")
    print("=" * 60)
    print()

    status, alerts = check_backups()

    # Print status
    print("\nBackup Status:")
    print(json.dumps(status, indent=2))

    # Send alerts if any
    if alerts:
        print("\n⚠️ Alerts:")
        for alert in alerts:
            print(f"  {alert}")

        # Send Telegram notification
        message = "🚨 *Backup Alert*\n\n" + "\n".join(alerts)
        send_telegram(message)

        return 1
    else:
        print("\n✅ All backups are current")
        return 0


if __name__ == "__main__":
    sys.exit(main())
