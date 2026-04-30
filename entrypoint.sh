#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate

echo "Creating cache table..."
python manage.py createcachetable

# Run collectstatic if needed
if [ "$RUN_COLLECTSTATIC" = "True" ]; then
    echo "Collecting static..."
    python manage.py collectstatic --noinput
fi

echo "Starting server..."

exec "$@"
