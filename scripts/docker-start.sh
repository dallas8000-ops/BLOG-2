#!/bin/sh
set -e
echo "[blog-2] migrate..."
python manage.py migrate --noinput || echo "[blog-2] WARN: migrate failed — starting gunicorn anyway"
PORT="${PORT:-8080}"
echo "[blog-2] gunicorn on 0.0.0.0:${PORT}"
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT}" --workers 2 --timeout 120 --access-logfile - --error-logfile -
