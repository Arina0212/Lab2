#!/bin/bash

# Ожидание готовности RabbitMQ
echo "Waiting for RabbitMQ..."
while ! nc -z rabbitmq 5672; do
    sleep 0.1
done
echo "RabbitMQ is ready!"

# Применение миграций
echo "Applying database migrations..."
alembic upgrade head

# Запуск приложения
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
