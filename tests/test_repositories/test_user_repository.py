import pytest

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class TestUserRepository:

    @pytest.fixture
    def repository(self):
        return UserRepository()

    @pytest.fixture
    def user_data(self):
        return UserCreate(email="test@example.com", name="Test User")

    async def test_create_user(self, repository, session, user_data):
        # Act
        user = await repository.create(session, user_data)

        # Assert
        assert user.id is not None
        assert user.email == user_data.email
        assert user.name == user_data.name

    async def test_get_user_by_id(self, repository, session, user_data):
        # Arrange
        created_user = await repository.create(session, user_data)

        # Act
        found_user = await repository.get_by_id(session, created_user.id)

        # Assert
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == user_data.email

    async def test_get_user_by_id_not_found(self, repository, session):
        # Act
        user = await repository.get_by_id(session, 999)

        # Assert
        assert user is None

    async def test_get_users_by_filter(self, repository, session, user_data):
        # Arrange
        await repository.create(session, user_data)

        # Act
        users = await repository.get_by_filter(session, count=10, page=1)

        # Assert
        assert len(users) == 1
        assert users[0].email == user_data.email

    async def test_update_user(self, repository, session, user_data):
        # Arrange
        created_user = await repository.create(session, user_data)
        update_data = UserUpdate(name="Updated Name")

        # Act
        updated_user = await repository.update(session, created_user.id, update_data)

        # Assert
        assert updated_user.name == "Updated Name"
        assert updated_user.email == user_data.email

    async def test_delete_user(self, repository, session, user_data):
        # Arrange
        created_user = await repository.create(session, user_data)

        # Act
        await repository.delete(session, created_user.id)

        # Assert
        deleted_user = await repository.get_by_id(session, created_user.id)
        assert deleted_user is None
