#!/bin/bash
# Schedule daily contest cache refresh at 12:01 AM IST.
# Add to crontab with: crontab -e
# 1 0 * * * /path/to/Recursioncursor/backend/scripts/refresh_contest_cache.sh >> /var/log/contest_cache.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MANAGE_PY="$PROJECT_DIR/website/manage.py"

cd "$PROJECT_DIR/website"
python "$MANAGE_PY" refresh_contest_cache --force
