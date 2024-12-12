# db.taskCRUD.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import TaskInDB
from app.data import Task


async def get_all_task(session: AsyncSession, page_size: int, page_number: int) -> list:
    result = await session.execute(select(TaskInDB).limit(page_size).offset(page_number - 1))
    return result.scalars().all()


async def add_task(session: AsyncSession, task: Task) -> TaskInDB:
    task_dict = task.dict(exclude={'id'})
    new_task = TaskInDB(**task_dict)
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task


async def delete_task(session: AsyncSession, task_id: int) -> TaskInDB:
    result = await session.execute(select(TaskInDB).where(TaskInDB.id == task_id))
    task = result.scalar_one()
    await session.delete(task)
    await session.commit()
    return task


async def finish_task(session: AsyncSession, task_id: int) -> TaskInDB:
    result = await session.execute(select(TaskInDB).where(TaskInDB.id == task_id))
    task = result.scalar_one()
    task.is_finished = 1
    await session.commit()
    return task
