from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:

    async def get_by_id(self, session: AsyncSession, user_id: int) -> User | None:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_filter(self, session: AsyncSession, count: int, page: int, **kwargs) -> list[User]:
        query = select(User)
        
        for key, value in kwargs.items():
            if hasattr(User, key):
                query = query.where(getattr(User, key) == value)
        
        offset_val = (page - 1) * count
        query = query.offset(offset_val).limit(count)
        
        result = await session.execute(query)
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, user_data: UserCreate) -> User:
        db_user = User(**user_data.model_dump())
        session.add(db_user)
        await session.flush()
        await session.refresh(db_user)
        return db_user

    async def update(self, session: AsyncSession, user_id: int, user_data: UserUpdate) -> User:
        user = await self.get_by_id(session, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user

    async def delete(self, session: AsyncSession, user_id: int) -> None:
        user = await self.get_by_id(session, user_id)
        if user:
            await session.delete(user)
            await session.flush()

    async def get_total_count(self, session: AsyncSession, **kwargs) -> int:
        query = select(func.count(User.id))
        for key, value in kwargs.items():
            if hasattr(User, key):
                query = query.where(getattr(User, key) == value)
        result = await session.execute(query)
        return result.scalar_one()