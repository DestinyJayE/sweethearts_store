# routers.user.py
import pydantic
from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.data import APIResult
from app.db import userCRUD  # 导入 CRUD 方法
from app.db.session import get_db_session  # 导入 session 依赖
from app.util import create_access_token

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
        return APIResult.error(code="429", msg=str(e))
