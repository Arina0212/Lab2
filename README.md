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
