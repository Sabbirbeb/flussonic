import pytest

from app.domain import User, TaskStatus
from app.application import schemas
from app.infrastructure.uow import UnitOfWork
from app.transport.schemas import CreateTask, UpdateTask

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
            result = await uow.tasks.create(
                schemas.TaskCreate(
                    user_id=user.id,
                    status=TaskStatus.WAITING,
                    title="test_title",
                    description="test_description",
                ))
            await uow.commit()
        
        async with httpx.AsyncClient() as session:
            response = await session.get(
                "http://0.0.0.0:9000/api/v1/tasks",
                follow_redirects=True,
                headers={"Authorization": f"Bearer {user.name}"},
            )
        
        assert result
        assert response.status_code == 200
        assert len(response.json()) != 0


    async def test_get_by_id(self, user: User, uow: UnitOfWork) -> None:  # noqa: ANN001
        async with uow:
            result = await uow.tasks.create(
                schemas.TaskCreate(
                    user_id=user.id,
                    status=TaskStatus.WAITING,
                    title="test_title",
                    description="test_description",
                ))
            await uow.commit()
        
        async with httpx.AsyncClient() as session:
            response = await session.get(
                f"http://0.0.0.0:9000/api/v1/tasks/{result.id}",
                follow_redirects=True,
                headers={"Authorization": f"Bearer {user.name}"},
            )
        
        assert result
        assert response.status_code == 200
        assert len(response.json()) != 0


    async def test_put(self, user: User, uow: UnitOfWork) -> None:  # noqa: ANN001
        async with uow:
            result = await uow.tasks.create(
                schemas.TaskCreate(
                    user_id=user.id,
                    status=TaskStatus.WAITING,
                    title="test_title",
                    description="test_description",
                ))
            await uow.commit()
        
        async with httpx.AsyncClient() as session:
            response = await session.put(
                f"http://0.0.0.0:9000/api/v1/tasks/{result.id}",
                follow_redirects=True,
                headers={"Authorization": f"Bearer {user.name}"},
                json=UpdateTask(title="test_title",
                                description="test_desc_updated",
                                status=TaskStatus.PROCESSING).model_dump_json()
            )
        
        assert result
        assert response.status_code == 200
        assert len(response.json()) != 0
        assert response.json().get("id") == result.id
        assert response.json().get("description") == "test_desc_updated"
        assert response.json().get("status") == "processing"


    async def test_delete(self, user: User, uow: UnitOfWork, admin: User) -> None:  # noqa: ANN001
        async with uow:
            result_user_1 = await uow.tasks.create(
                schemas.TaskCreate(
                    user_id=user.id,
                    status=TaskStatus.WAITING,
                    title="test_title",
                    description="test_description",
                ))
            await uow.commit()

            result_user_2 = await uow.tasks.create(
                schemas.TaskCreate(
                    user_id=user.id,
                    status=TaskStatus.WAITING,
                    title="test_title",
                    description="test_description",
                ))
            await uow.commit()

            result_admin = await uow.tasks.create(
                schemas.TaskCreate(
                    user_id=admin.id,
                    status=TaskStatus.WAITING,
                    title="test_title",
                    description="test_description",
                ))
            await uow.commit()
        
        async with httpx.AsyncClient() as session:
            response = await session.delete(
                f"http://0.0.0.0:9000/api/v1/tasks/{result_user_1.id}",
                follow_redirects=True,
                headers={"Authorization": f"Bearer {user.name}"},
            )
            assert response.status_code == 204

            response = await session.delete(
                f"http://0.0.0.0:9000/api/v1/tasks/{result_admin.id}",
                follow_redirects=True,
                headers={"Authorization": f"Bearer {user.name}"},
            )
            assert response.status_code == 403

            response = await session.delete(
                f"http://0.0.0.0:9000/api/v1/tasks/{result_admin.id}",
                follow_redirects=True,
                headers={"Authorization": f"Bearer {admin.name}"},
            )
            assert response.status_code == 204

            response = await session.delete(
                f"http://0.0.0.0:9000/api/v1/tasks/{result_user_2.id}",
                follow_redirects=True,
                headers={"Authorization": f"Bearer {admin.name}"},
            )
            assert response.status_code == 204
