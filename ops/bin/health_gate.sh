#!/usr/bin/env bash
set -euo pipefail

BASE="${1:-${API_BASE:-}}"
if [[ -z "$BASE" ]]; then
  echo "Usage: $0 [API_BASE]"
  echo "Example: API_BASE=https://your.service ops/bin/health_gate.sh"
  exit 1
fi

for endpoint in "/health" "/version" "/api/scan?limit=1"; do
  echo
  echo "→ GET ${BASE}${endpoint}"
  curl -fsS "${BASE}${endpoint}"
done
