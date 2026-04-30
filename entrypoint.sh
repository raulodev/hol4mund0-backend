#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate

echo "Creating cache table..."
python manage.py createcachetable

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "Starting server..."

exec "$@"
