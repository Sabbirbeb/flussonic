import pytest

from app.domain import User
from app.infrastructure.uow import UnitOfWork
from app.transport.schemas import CreateTask

from httpx import AsyncClient
import httpx


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

    async def test_create(self, user: User, uow: UnitOfWork) -> None:  # noqa: ANN001
        async with httpx.AsyncClient() as session:
            response = await session.post(
                "http://0.0.0.0:9000/api/v1/tasks",
                follow_redirects=True,
                headers={"Authorization": f"Bearer {user.name}"},
                json=CreateTask(title="test_title",
                                description="test_desc").model_dump_json()
            )

        async with uow:
            result = await uow.tasks.get(response.json().get('id'))
        
        assert response.status_code == 201
        assert result.title == "test_title"
        assert result.description == "test_desc"
    
    async def test_get(self, user: User, uow: UnitOfWork) -> None:  # noqa: ANN001
        async with uow:
            result = await uow.tasks.create(response.json().get('id'))
        
        print (result)
        async with httpx.AsyncClient() as session:
            response = await session.get(
                "http://0.0.0.0:9000/api/v1/tasks",
                follow_redirects=True,
                headers={"Authorization": f"Bearer {user.name}"},
            )

            print (response.json())

        
        assert response.status_code == 200
        assert result.title == "test_title"
        assert result.description == "test_desc"

