import asyncio
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from litestar import Litestar
from litestar.di import Provide
from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.controllers.user_controller import UserController
from app.models.user import Base
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(engine):
    async_session = async_sessionmaker(engine, class_=AsyncSession)
    async with async_session() as session:
        yield session


@pytest.fixture
def app(engine):
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
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return Litestar(
        route_handlers=[UserController],
        dependencies={
            "db_session": Provide(provide_db_session),
            "user_repository": Provide(provide_user_repository, sync_to_thread=False),
            "user_service": Provide(provide_user_service, sync_to_thread=False),
        },
        on_startup=[on_startup],
    )


@pytest.fixture
def client(app):
    return TestClient(app=app)


@pytest.fixture
def user_data():
    return {"email": "test@example.com", "name": "Test User"}
