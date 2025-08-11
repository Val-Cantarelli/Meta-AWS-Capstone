#!/usr/bin/env bash
set -euo pipefail

# Load environment variables from .env if present
if [ -f ".env" ]; then
  set -a
  . ./.env
  set +a
fi

# Ensure local settings by default
unset DJANGO_ENV || true
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-core.settings.local}"

# Optional notice if API_BASE_URL isn't set
if [ -z "${API_BASE_URL:-}" ]; then
  echo "Warning: API_BASE_URL is not set. Define it in .env to point to your API." >&2
fi

python manage.py runserver