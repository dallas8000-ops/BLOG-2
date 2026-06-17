#!/bin/sh
set -e

echo "[blog-2] migrate..."
if ! python manage.py migrate --noinput 2>/tmp/migrate.err; then
  if grep -q 'accounts_profile' /tmp/migrate.err; then
    echo "[blog-2] repairing accounts migration state (tables missing)..."
    python manage.py migrate accounts zero --fake
    python manage.py migrate --noinput
  else
    cat /tmp/migrate.err >&2
    echo "[blog-2] WARN: migrate failed — starting gunicorn anyway"
  fi
fi

PORT="${PORT:-8080}"
echo "[blog-2] gunicorn on 0.0.0.0:${PORT}"
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT}" --workers 2 --timeout 120 --access-logfile - --error-logfile -
