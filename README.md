## 1. Активация виртуального окружения
```bash
cd D:\Lab2
venv\Scripts\activate
pip install litestar sqlalchemy aiosqlite uvicorn pydantic python-dotenv email-validator
python run.py
```
Откроется на http://localhost:8000/users
## 2.  API Endpoints
### Создание пользователя
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"test@example.com\", \"name\": \"John Doe\"}"
```
### Получить всех пользователей
```bash
curl "http://localhost:8000/users"
```
### Получить пользователя по ID
```bash
curl "http://localhost:8000/users/1"
```
### Обновить пользователя
```bash
curl -X PUT "http://localhost:8000/users/1" -H "Content-Type: application/json" -d "{\"name\": \"Updated Name\"}"
```
### Удалить пользователя
```bash
curl -X DELETE "http://localhost:8000/users/1"
```
## 3. Тестирование приложения
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```
### Запуск тестов
```bash
# Все тесты
pytest

# Только тесты репозиториев
pytest tests/test_repositories/

# Только тесты сервисов
pytest tests/test_services/

# Только тесты API
pytest tests/test_controllers/

# С подробным выводом
pytest -v

# С выводом print-ов
pytest -s

# С покрытием кода
pytest --cov=app --cov-report=html
```
## 4. Настройка pre-commit
```bash
pre-commit install
pre-commit run --all-files
```

## 5. Запуск в Docker
```bash
docker-compose up --build
```
Адрес http://localhost:8000/users
