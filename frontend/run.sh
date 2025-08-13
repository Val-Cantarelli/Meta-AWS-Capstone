#!/usr/bin/env bash

# New terminal, RUN this script to start the frontend server.
# run.sh — execution profiles for dev/prod with local HTTPS by default.
#python -m venv .venv
#source .venv/bin/activate
#pip install pip-tools
#pip-sync requirements-dev.txt
#./run.sh

# If added somenthing to in requirements-dev.in, run:
#pip-compile -o requirements-dev.txt requirements-dev.in
#pip-sync requirements-dev.txt




set -euo pipefail

# Load .env 
if [ -f ".env" ]; then set -a; . ./.env; set +a; fi

# Profiles and defaults
PROFILE="${1:-${PROFILE:-local}}" # local | local-http | prod
HOST="${HOST:-localhost}"
PORT="${PORT:-8000}" # HTTP port (local-http, prod)
SSL_PORT="${SSL_PORT:-8443}" # HTTPS port (local)
DJANGO_LOCAL_SETTINGS="${DJANGO_LOCAL_SETTINGS:-core.settings.local}"
DJANGO_PROD_SETTINGS="${DJANGO_PROD_SETTINGS:-core.settings.production}"
CERT_DIR="${CERT_DIR:-.certs}"
CERT_FILE="${CERT_FILE:-$CERT_DIR/localhost.pem}"
KEY_FILE="${KEY_FILE:-$CERT_DIR/localhost-key.pem}"
API_BASE_URL_PRINT="${API_BASE_URL:-<not set>}"
ASGI_APP="${ASGI_APP:-core.asgi:application}"  # adjust if your ASGI module is different

command_exists() { command -v "$1" >/dev/null 2>&1; }
have_mod() { python -c "import $1" >/dev/null 2>&1; }

open_url() {
    local url="$1"
    if command_exists open; then ( sleep 1; open -g "$url" ) >/dev/null 2>&1 || true
    elif command_exists xdg-open; then ( sleep 1; xdg-open "$url" ) >/dev/null 2>&1 || true
    fi
}

ensure_certs() {
    mkdir -p "$CERT_DIR"
    if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then return 0; fi

    echo ">> Generating certificates in $CERT_DIR ..."
    if command_exists mkcert; then
        mkcert -install >/dev/null 2>&1 || true
        mkcert -key-file "$KEY_FILE" -cert-file "$CERT_FILE" localhost 127.0.0.1 ::1
    else
        echo ">> mkcert not found; generating self-signed with openssl (browser may warn)."
        openssl req -x509 -nodes -newkey rsa:2048 \
            -keyout "$KEY_FILE" -out "$CERT_FILE" -days 365 \
            -subj "/CN=localhost" \
            -addext "subjectAltName=DNS:localhost,IP:127.0.0.1" >/dev/null 2>&1
    fi
    echo ">> Certificate ready: $CERT_FILE"
}

run_local_https() {
    export DJANGO_SETTINGS_MODULE="$DJANGO_LOCAL_SETTINGS"
    echo "Profile: local (HTTPS)"
    echo "DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE"
    echo "API_BASE_URL=${API_BASE_URL_PRINT}"
    echo ">> Include https://$HOST:$SSL_PORT in CSRF_TRUSTED_ORIGINS in local settings (if using CSRF)."

    ensure_certs
    local url="https://${HOST}:${SSL_PORT}"
    open_url "$url"

    # Path A: runserver_plus (django-extensions + pyOpenSSL)
    if have_mod django_extensions && have_mod OpenSSL; then
        echo ">> Starting runserver_plus (TLS) at $url"
        exec python manage.py runserver_plus \
            --cert-file "$CERT_FILE" --key-file "$KEY_FILE" \
            "${HOST}:${SSL_PORT}"
    fi

    # Path B: Uvicorn (ASGI) with TLS
    if have_mod uvicorn; then
        echo ">> Starting Uvicorn (TLS) at $url"
        exec uvicorn "$ASGI_APP" \
            --host "$HOST" --port "$SSL_PORT" \
            --ssl-certfile "$CERT_FILE" --ssl-keyfile "$KEY_FILE" \
            --reload
    fi

    echo "ERROR: install one of the local TLS options:"
    echo "  pip install django-extensions pyOpenSSL"
    echo "  # or"
    echo "  pip install uvicorn"
    exit 2
}

run_local_http() {
    export DJANGO_SETTINGS_MODULE="$DJANGO_LOCAL_SETTINGS"
    echo "Profile: local-http (no TLS)"
    echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}"
    echo "API_BASE_URL=${API_BASE_URL_PRINT}"
    local url="http://${HOST}:${PORT}"
    open_url "$url"
    exec python manage.py runserver "${HOST}:${PORT}"
}

run_prod_http() {
    export DJANGO_SETTINGS_MODULE="$DJANGO_PROD_SETTINGS"
    echo "Profile: prod (dev server is HTTP-only; HTTPS redirects may break local navigation)"
    echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}"
    echo "API_BASE_URL=${API_BASE_URL_PRINT}"
    python manage.py collectstatic --noinput
    exec python manage.py runserver "127.0.0.1:${PORT}"
}

case "${PROFILE}" in
    local|local-https) run_local_https ;;
    local-http)        run_local_http  ;;
    prod)              run_prod_http   ;;
    *) echo "Unknown profile: ${PROFILE} (use: local | local-http | prod)" >&2; exit 1 ;;
esac
