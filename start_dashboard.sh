#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

PORT=${PORT:-8090}
HOST=${HOST:-0.0.0.0}

echo "=== Starting AAS-Sec Red Team Swarm Dashboard on ${HOST}:${PORT} ==="

# Kill existing uvicorn instance on port 8090 if running
fuser -k ${PORT}/tcp 2>/dev/null || true

exec ./venv/bin/uvicorn dashboard.app:app --host "$HOST" --port "$PORT"
