from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from litestar.params import Body, Parameter
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserListResponse, UserResponse, UserUpdate
from app.services.user_service import UserService


class UserController(Controller):
    path = "/users"

    @get("/{user_id:int}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        db_session: AsyncSession,
        user_id: int = Parameter(gt=0),
    ) -> UserResponse:
        user = await user_service.get_by_id(db_session, user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        db_session: AsyncSession,
        count: int = Parameter(ge=1, default=10),
        page: int = Parameter(ge=1, default=1),
    ) -> UserListResponse:
        users = await user_service.get_by_filter(db_session, count=count, page=page)
        total = await user_service.get_total_count(db_session)
        return UserListResponse(
            users=[UserResponse.model_validate(user) for user in users],
            total_count=total,
        )

    @post()
    async def create_user(
        self,
        user_service: UserService,
        db_session: AsyncSession,
        data: UserCreate = Body(),
    ) -> UserResponse:
        user = await user_service.create(db_session, data)
        await db_session.commit()
        return UserResponse.model_validate(user)

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        user_service: UserService,
        db_session: AsyncSession,
        user_id: int,
    ) -> None:
        await user_service.delete(db_session, user_id)
        await db_session.commit()

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        db_session: AsyncSession,
        user_id: int,
        data: UserUpdate = Body(),
    ) -> UserResponse:
        user = await user_service.update(db_session, user_id, data)
        await db_session.commit()
        return UserResponse.model_validate(user)
