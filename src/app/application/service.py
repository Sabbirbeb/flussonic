from app import domain
from app.application import errors, schemas
from app.application.interface import IUnitOfWork


class TaskService:
    def __init__(
        self,
        uow: IUnitOfWork,
    ) -> None:
        self.uow: IUnitOfWork = uow

    async def create_task(self, task: domain.Task, user: str) -> domain.Task:
        async with self.uow:
            task = (
                await self.uow.tasks.create(
                    schemas.TaskCreate(
                        title=task.title,
                        description=task.description,
                        status=domain.Task.CREATED,
                        user_id=user.id,
                    )
                ),
            )
            await self.uow.commit()
        return task

    async def update_task(self, task_id: int, dto: schemas.TaskUpdate) -> domain.Task:
        async with self.uow:
            batch = await self.uow.tasks.update(task_id, dto)
            if not batch:
                raise errors.NotFoundError
            await self.uow.commit()

        return batch

    async def get_tasks(self, skip: int, limit: int) -> list[domain.Task]:
        async with self.uow:
            return await self.uow.tasks.list(skip, limit)

    async def get_task(self, task_id: int) -> domain.Task:
        async with self.uow:
            batch = await self.uow.batches.get(task_id)
        if not batch:
            raise errors.NotFoundError

        return batch

    # async def get_subscriptions(
    #     self, skip: int, limit: int
    # ) -> list[domain.Subscription]:
    #     async with self.uow:
    #         return await self.uow.subs.list(skip, limit)

    async def get_user(self, user_id: id) -> domain.User:
        async with self.uow:
            user = await self.uow.users.get(user_id)
        if not user:
            raise errors.NotFoundError

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