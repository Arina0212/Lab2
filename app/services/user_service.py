from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, session: AsyncSession, user_id: int) -> User | None:
        return await self.user_repository.get_by_id(session, user_id)

    async def get_by_filter(
        self, session: AsyncSession, count: int, page: int, **kwargs
    ) -> list[User]:
        return await self.user_repository.get_by_filter(session, count, page, **kwargs)

    async def create(self, session: AsyncSession, user_data: UserCreate) -> User:
        # Проверка уникальности email
        existing_users = await self.user_repository.get_by_filter(
            session, count=1, page=1, email=user_data.email
        )
        if existing_users:
            raise ValueError(f"User with email {user_data.email} already exists")

        return await self.user_repository.create(session, user_data)

    async def update(
        self, session: AsyncSession, user_id: int, user_data: UserUpdate
    ) -> User:
        return await self.user_repository.update(session, user_id, user_data)

    async def delete(self, session: AsyncSession, user_id: int) -> None:
        await self.user_repository.delete(session, user_id)

    async def get_total_count(self, session: AsyncSession, **kwargs) -> int:
        return await self.user_repository.get_total_count(session, **kwargs)
