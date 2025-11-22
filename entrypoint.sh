#!/bin/bash

# Ожидание готовности базы данных
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done
echo "Database is ready!"

# Применение миграций
echo "Applying database migrations..."
alembic upgrade head

# Запуск приложения
echo "Starting application..."
exec uvicorn --reload --host $HOST --port $PORT --log-level debug app.main:app
