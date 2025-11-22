from unittest.mock import AsyncMock, MagicMock

import pytest

from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


class TestUserService:

    @pytest.fixture
    def mock_repository(self):
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repository):
        return UserService(mock_repository)

    @pytest.fixture
    def user_data(self):
        return UserCreate(email="test@example.com", name="Test User")

    @pytest.fixture
    def mock_user(self):
        user = MagicMock()
        user.id = 1
        user.email = "test@example.com"
        user.name = "Test User"
        return user

    async def test_create_user_success(
        self, service, mock_repository, user_data, mock_user
    ):
        # Arrange
        mock_repository.get_by_filter.return_value = []
        mock_repository.create.return_value = mock_user

        # Act
        result = await service.create(None, user_data)

        # Assert
        assert result == mock_user
        mock_repository.get_by_filter.assert_called_once()
        mock_repository.create.assert_called_once_with(None, user_data)

    async def test_create_user_duplicate_email(
        self, service, mock_repository, user_data, mock_user
    ):
        # Arrange
        mock_repository.get_by_filter.return_value = [mock_user]

        # Act & Assert
        with pytest.raises(ValueError, match="already exists"):
            await service.create(None, user_data)

    async def test_get_user_by_id(self, service, mock_repository, mock_user):
        # Arrange
        mock_repository.get_by_id.return_value = mock_user

        # Act
        result = await service.get_by_id(None, 1)

        # Assert
        assert result == mock_user
        mock_repository.get_by_id.assert_called_once_with(None, 1)

    async def test_update_user(self, service, mock_repository, mock_user):
        # Arrange
        update_data = UserUpdate(name="Updated Name")
        mock_repository.update.return_value = mock_user

        # Act
        result = await service.update(None, 1, update_data)

        # Assert
        assert result == mock_user
        mock_repository.update.assert_called_once_with(None, 1, update_data)

    async def test_delete_user(self, service, mock_repository):
        # Act
        await service.delete(None, 1)

        # Assert
        mock_repository.delete.assert_called_once_with(None, 1)
