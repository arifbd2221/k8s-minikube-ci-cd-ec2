#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi


# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

if [ "$APP_ENV" = "development" ]; then
    # Use Uvicorn with auto-reload for development
    echo "Starting server in development mode with Uvicorn $APP_ENV"
    exec uvicorn main.asgi:application --host 0.0.0.0 --port "$DJANGO_PORT" --reload
else
    # Use Gunicorn for production
    echo "Starting server in production mode with Gunicorn $APP_ENV"
    exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker main.asgi:application --bind 0.0.0.0:"$DJANGO_PORT"
fi
