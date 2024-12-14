# routers.user.py
from pydantic import Field

from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.data import APIResult, Task
from app.db import get_db_session, taskCRUD, userCRUD
from app.util import get_user_id_from_token

router = APIRouter()


@router.get("/self_task", response_model=APIResult[list[Task]])
async def get_self_task(
        page_number: int = 1,
        page_size: int = 10,
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session)
) -> APIResult[list[Task]]:
    try:
        task_list = await taskCRUD.get_user_task(session, user_id=user_id, page_size=page_size, page_number=page_number)
        return APIResult.success(data=task_list)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.get("/sweetheart_task", response_model=APIResult[list[Task]])
async def get_sweetheart_task(
        page_number: int = 1,
        page_size: int = 10,
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session)
) -> APIResult[list[Task]]:
    try:
        user = await userCRUD.get_user(session, user_id)
        task_list = await taskCRUD.get_user_task(session, user_id=user.sweetheart_id, page_size=page_size,
                                                 page_number=page_number)
        return APIResult.success(data=task_list)
    except Exception as e:
        return APIResult.error(msg=str(e))


class AddTaskReq(BaseModel):
    name: str = Field(default="", title="任务名称")
    price: int = Field(default=0, title="任务奖励")
    des: str = Field(default="", title="任务描述")


@router.post("/add", response_model=APIResult[Task])
async def add_task(
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session),
        req: AddTaskReq = Body()
) -> APIResult[Task]:
    try:
        task_dict = req.dict()
        task_dict["create_id"] = user_id
        task_dict["is_finish"] = 0
        async with session.begin():
            new_task = await taskCRUD.add_task(session, Task(**task_dict))
        return APIResult.success(data=new_task)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.post("/delete", response_model=APIResult[Task])
async def delete_task(
        id: int,
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session),
) -> APIResult[Task]:
    try:
        async with session.begin():
            deleted_task = await taskCRUD.delete_task(session, id)
        return APIResult.success(data=deleted_task)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.post("/finish", response_model=APIResult[Task])
async def finish_task(
        id: int,
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session),
) -> APIResult[Task]:
    try:
        async with session.begin():
            finished_task = await taskCRUD.finish_task(session, id)
            await userCRUD.add_user_point(session, user_id=user_id, point=finished_task.price)
        return APIResult.success(data=finished_task)
    except Exception as e:
        return APIResult[Task].error(msg=str(e))
