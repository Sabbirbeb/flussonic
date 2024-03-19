from app import domain
from app.application import errors, schemas
from app.application.interface import IUnitOfWork


class TaskService:
    def __init__(
        self,
        uow: IUnitOfWork,
    ) -> None:
        self.uow: IUnitOfWork = uow

    async def create_task(self, task: schemas.TaskCreate) -> domain.Task:
        async with self.uow:
            task = await self.uow.tasks.create(
                schemas.TaskCreate(
                    title=task.title,
                    description=task.description,
                    status=domain.TaskStatus.WAITING,
                    user_id=task.user_id,
                ),
            )
            await self.uow.commit()
        return task

    async def update_task(self, task_id: int, dto: schemas.TaskUpdate, user: schemas.User) -> domain.Task:
        async with self.uow:
            task = await self.uow.tasks.get(task_id)
            if not task:
                raise errors.NotFoundError
            if task.user_id == user.id or user.admin:
                task = await self.uow.tasks.update(task_id, dto)
                await self.uow.commit()
            else:
                raise errors.NoPermissionError

        return task

    async def get_tasks(self) -> list[domain.Task]:
        async with self.uow:
            return await self.uow.tasks.list()

    async def get_task(self, task_id: int) -> domain.Task:
        async with self.uow:
            task = await self.uow.tasks.get(task_id)
        if not task:
            raise errors.NotFoundError

        return task

    async def delete_task(self, task_id: int, user: schemas.User):
        async with self.uow:
            task = await self.uow.tasks.get(task_id)
            if not task:
                raise errors.NotFoundError
            if task.user_id == user.id or user.admin:
                await self.uow.tasks.delete(task_id)
                await self.uow.commit()
            else:
                raise errors.NoPermissionError

        return task

    # async def get_subscriptions(
    #     self, skip: int, limit: int
    # ) -> list[domain.Subscription]:
    #     async with self.uow:
    #         return await self.uow.subs.list(skip, limit)

    async def get_user(self, user: schemas.User) -> domain.User:
        async with self.uow:
            user = await self.uow.users.get(user.id)
        if not user:
            raise errors.NotFoundError

        return user

    async def get_users(self) -> list[domain.User]:
        async with self.uow:
            users = await self.uow.users.list()
        if not users:
            raise errors.NotFoundError

        return users

    async def create_user(self, dto: schemas.UserCreate) -> domain.User:
        async with self.uow:
            user = await self.uow.users.create(dto)
            await self.uow.commit()

        return user

    async def get_user_by_name(self, user_name: str) -> domain.User:
        async with self.uow:
            user = await self.uow.users.get_by_name(user_name)
        if not user:
            raise errors.NotFoundError

        return user

    async def update_user_to_admin(self, user: schemas.User) -> domain.User:
        async with self.uow:
            user = await self.uow.users.update(user.id, update_dto=schemas.UserUpdate(admin=True))
            await self.uow.commit()

        return user

    # async def update_or_create_admin(
    #     self,
    #     user: schemas.SubscriptionCreate,
    # ) -> list[domain.Subscription]:
    #     async with self.uow:
    #         subs = await self.uow.subs.list_by_id([sub.id for sub in subs_meta])
    #         batches = await self.uow.batches.list_by_id(
    #             {sub.batch_id for sub in subs_meta}
    #         )
    #         id_to_sub = {sub.id: sub for sub in subs}
    #         id_to_batch = {batch.id: batch for batch in batches}
    #         subs_dtos: list[schemas.SubscriptionCreate] = []
    #         for meta in subs_meta:
    #             sub = id_to_sub.get(meta.id)
    #             if not sub:
    #                 if not id_to_batch.get(meta.batch_id):
    #                     raise errors.NotFoundError

    #                 subs_dtos.append(meta)
    #             else:
    #                 sub = await self.uow.subs.update(
    #                     sub.id, schemas.SubscriptionUpdate(status=meta.status)
    #                 )
    #         subs = await self.uow.subs.bulk_create(subs_dtos)
    #         await self.uow.commit()
    #     return subs
