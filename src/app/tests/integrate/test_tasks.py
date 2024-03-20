from app.domain import User


class TestIntegrations:
    def test_health(self, test_client) -> None:  # noqa: ANN001
        response = test_client.get("/api/v1/health", follow_redirects=True)

        assert response.status_code == 200

    def test_no_bearer(self, test_client) -> None:  # noqa: ANN001
        response = test_client.get(
            "/api/v1/tasks",
            follow_redirects=True,
        )

        assert response.status_code == 403

    def test_no_authorization(self, test_client, unregisterd_user: User) -> None:  # noqa: ANN001
        response = test_client.get(
            "/api/v1/tasks",
            follow_redirects=True,
            headers={"Authorization": f"Bearer {unregisterd_user.name}"},
        )

        assert response.status_code == 403
