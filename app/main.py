import os
from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.controllers.user_controller import UserController
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.models.user import Base

# Настройка базы данных SQLite
DATABASE_URL = "sqlite+aiosqlite:///./lab3.db"

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    connect_args={"check_same_thread": False}
)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def provide_db_session() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

def provide_user_repository() -> UserRepository:
    return UserRepository()

def provide_user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)

async def on_startup():
    """Создание таблиц при запуске приложения"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
    on_startup=[on_startup]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)