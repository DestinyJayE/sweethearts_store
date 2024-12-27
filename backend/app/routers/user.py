# routers.user.py
import pydantic
from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.data import APIResult
from app.db import userCRUD  # 导入 CRUD 方法
from app.db.session import get_db_session  # 导入 session 依赖
from app.util import create_access_token, get_user_id_from_token

router = APIRouter()


class UserLoginReq(BaseModel):
    user_name: str = pydantic.Field(title="用户名")
    password: str = pydantic.Field(title="密码")


@router.post("/login", response_model=APIResult[dict])
async def login(
        session: AsyncSession = Depends(get_db_session),
        req: UserLoginReq = Body()
):
    try:
        user = await userCRUD.login(session, req.user_name, req.password)
        if user is None:
            return APIResult.error(code="429", msg="用户名或密码错误")
        else:
            user_dict = {"user_id": user.id}
            token = create_access_token(user_dict)
            return APIResult.success(data={"token": token})
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.get("/point", response_model=APIResult[int])
async def get_point(
        session: AsyncSession = Depends(get_db_session),
        user_id: int = Depends(get_user_id_from_token)
) -> APIResult[int]:
    try:
        user = await userCRUD.get_user(session, user_id)
        return APIResult.success(data=user.point)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.get("/sweetheart_point", response_model=APIResult[int])
async def get_sweetheart_point(
        session: AsyncSession = Depends(get_db_session),
        user_id: int = Depends(get_user_id_from_token)
) -> APIResult[int]:
    try:
        user = await userCRUD.get_user(session, user_id)
        sweetheart = await userCRUD.get_user(session, user.sweetheart_id)
        return APIResult.success(data=sweetheart.point)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.post("/update_password",response_model=APIResult[str])
async def update_password(
    new_password: str,
    session: AsyncSession = Depends(get_db_session),
    user_id: int = Depends(get_user_id_from_token)
) -> APIResult[str]:
    try:
        async with session.begin():
            user = await userCRUD.update_password(session, user_id, new_password)
        return APIResult.success(data="success")
    except Exception as e:
        return APIResult.error(msg=str(e))