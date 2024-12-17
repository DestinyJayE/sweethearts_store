# db.taskCRUD.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import TaskInDB
from app.data import Task


async def get_user_task(session: AsyncSession, user_id: int, page_size: int, page_number: int) -> list[Task]:
    result = await session.execute(
        select(TaskInDB).limit(page_size).offset(page_number - 1).where(TaskInDB.create_id == user_id))
    tasks = result.scalars().all()
    return [Task.from_orm(task) for task in tasks]


async def add_task(session: AsyncSession, task: Task) -> Task:
    task_dict = task.dict(exclude={'id'})
    new_task = TaskInDB(**task_dict)
    session.add(new_task)
    await session.flush()
    # await session.refresh(new_task)
    return Task.from_orm(new_task)


async def delete_task(session: AsyncSession, task_id: int) -> Task:
    result = await session.execute(select(TaskInDB).where(TaskInDB.id == task_id))
    task = result.scalar_one()
    await session.delete(task)
    return Task.from_orm(task)


async def finish_task(session: AsyncSession, task_id: int) -> Task:
    result = await session.execute(select(TaskInDB).where(TaskInDB.id == task_id))
    task = result.scalar_one()
    task.is_finish = 1
    session.add(task)
    return Task.from_orm(task)
