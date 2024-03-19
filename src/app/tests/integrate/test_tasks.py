import pytest

from app.domain import User

user_name = "Tem"
admin_name ="Admin"

class TestIntegrations:
    def test_health(self, test_client) -> None:  # noqa: ANN001
        response = test_client.get("/api/v1/health", follow_redirects=True)

        assert response.status_code == 200

    def test_create(self, test_client) -> None:  # noqa: ANN001
        response = test_client.get("/api/v1/tasks", follow_redirects=True,
                                    headers = {'Authorization': f'Bearer {user_name}'})

        print (response.text)

        assert response.status_code == 200

