# routers.user.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud import create_user  # 导入 CRUD 方法
from app.db.session import get_db_session  # 导入 session 依赖
from app.data import APIResult,User

router = APIRouter()


# 添加用户接口
@router.post("/add",response_model=APIResult[User])
async def add_user(
        session: AsyncSession = Depends(get_db_session),
        req:User = Body()
):
    try:
        # 调用 CRUD 方法创建新用户
        new_user = await create_user(session, req.name, req.email, req.password)
        return APIResult.success(new_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
