import pytest

from app.domain import User
from app.infrastructure.uow import UnitOfWork
from app.transport.schemas import CreateTask

from httpx import AsyncClient


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

    @pytest.mark.asyncio()
    async def test_create(self, client: AsyncClient, user: User, uow: UnitOfWork) -> None:  # noqa: ANN001
        print (CreateTask(title="test_title",
                            description="test_desc").model_dump_json())
        response = await client.post(
            "/api/v1/tasks",
            follow_redirects=True,
            headers={"Authorization": f"Bearer {user.name}"},
            json=CreateTask(title="test_title",
                            description="test_desc").model_dump_json()
        )
        async with uow:
            result = await uow.tasks.list()
        
        print (result)


        assert response.status_code == 201
        assert response.desciption == "Task created successfully"

