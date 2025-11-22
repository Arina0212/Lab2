import pytest


class TestUserController:

    def test_create_user_success(self, client, user_data):
        # Act
        response = client.post("/users", json=user_data)

        # Debug:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]
        assert "id" in data

    def test_create_user_invalid_data(self, client):
        # Arrange
        invalid_data = {"email": "invalid-email", "name": "T"}

        # Act
        response = client.post("/users", json=invalid_data)

        # Assert
        assert response.status_code == 400

    def test_get_user_by_id_success(self, client, user_data):
        # Arrange
        create_response = client.post("/users", json=user_data)

        # Debug
        if create_response.status_code != 201:
            print(
                f"Create failed: {create_response.status_code} - {create_response.text}"
            )
            pytest.fail(
                f"User creation failed with status {create_response.status_code}"
            )

        user_id = create_response.json()["id"]

        # Act
        response = client.get(f"/users/{user_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == user_data["email"]

    def test_get_user_by_id_not_found(self, client):
        # Act
        response = client.get("/users/999")

        # Assert
        assert response.status_code == 404

    def test_get_all_users(self, client, user_data):
        # Arrange
        create_response = client.post("/users", json=user_data)

        if create_response.status_code != 201:
            print(
                f"Create failed: {create_response.status_code} - {create_response.text}"
            )
            pytest.fail(
                f"User creation failed with status {create_response.status_code}"
            )

        # Act
        response = client.get("/users?count=10&page=1")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "total_count" in data
        assert len(data["users"]) >= 1

    def test_update_user(self, client, user_data):
        # Arrange
        create_response = client.post("/users", json=user_data)

        if create_response.status_code != 201:
            print(
                f"Create failed: {create_response.status_code} - {create_response.text}"
            )
            pytest.fail(
                f"User creation failed with status {create_response.status_code}"
            )

        user_id = create_response.json()["id"]
        update_data = {"name": "Updated Name"}

        # Act
        response = client.put(f"/users/{user_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"

    def test_delete_user(self, client, user_data):
        # Arrange
        create_response = client.post("/users", json=user_data)

        if create_response.status_code != 201:
            print(
                f"Create failed: {create_response.status_code} - {create_response.text}"
            )
            pytest.fail(
                f"User creation failed with status {create_response.status_code}"
            )

        user_id = create_response.json()["id"]

        # Act
        response = client.delete(f"/users/{user_id}")

        # Assert
        assert response.status_code == 204

        # Проверяем, что пользователь удален
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
