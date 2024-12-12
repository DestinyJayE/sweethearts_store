# routers.user.py
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.data import APIResult, Task
from app.db import get_db_session, taskCRUD, userCRUD

router = APIRouter()


@router.get("/all", response_model=APIResult[list[Task]])
async def get_task(
        page_number: int = 1,
        page_size: int = 10,
        session: AsyncSession = Depends(get_db_session)
) -> APIResult[list[Task]]:
    try:
        task_list = await taskCRUD.get_all_task(session, page_size=page_size, page_number=page_number)
        return APIResult.success(data=task_list)
    except Exception as e:
        return APIResult.error(message=str(e))


@router.post("/add", response_model=APIResult[Task])
async def add_task(
        session: AsyncSession = Depends(get_db_session),
        req: Task = Body()
):
    try:
        new_task = await taskCRUD.add_task(session, req)
        return APIResult.success(data=new_task)
    except Exception as e:
        return APIResult.error(message=str(e))


@router.post("/delete", response_model=APIResult[Task])
async def delete_task(
        id: int,
        session: AsyncSession = Depends(get_db_session),
) -> APIResult[Task]:
    try:
        deleted_task = await taskCRUD.delete_task(session, id)
        return APIResult.success(data=deleted_task)
    except Exception as e:
        return APIResult.error(message=str(e))


@router.post("/finish", response_model=APIResult[Task])
async def finish_task(
        task_id: int,
        session: AsyncSession = Depends(get_db_session),
) -> APIResult[Task]:
    try:
        finished_task = await taskCRUD.finish_task(session, task_id)
        await userCRUD.add_user_point(session, finished_task.user_id, finished_task.price)
        return APIResult.success(data=finished_task)
    except Exception as e:
        return APIResult.error(message=str(e))