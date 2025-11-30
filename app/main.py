from fastapi import FastAPI

from app import models
from app.api.endpoints import router as api_router
from app.database import Base, engine

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Management System")

# Подключение роутеров API
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Order Management System API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
