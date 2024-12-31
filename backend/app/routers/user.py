# routers.user.py
import pydantic
from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.data import APIResult
from app.db import userCRUD,verificationCodeCRUD  # 导入 CRUD 方法
from app.db.session import get_db_session  # 导入 session 依赖
from app.util import create_access_token, get_user_id_from_token

router = APIRouter()

CODE_EXPIRATION_MINUTES = 10


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



class PointResp(BaseModel):
    point:int = pydantic.Field(title="自己分数")
    sweetheart_point:int = pydantic.Field(title="sweetheart分数")

@router.get("/point", response_model=APIResult[PointResp])
async def get_point(
        session: AsyncSession = Depends(get_db_session),
        user_id: int = Depends(get_user_id_from_token)
) -> APIResult[PointResp]:
    try:
        user = await userCRUD.get_user(session, user_id)
        sweetheart = await userCRUD.get_user(session,user.sweetheart_id)
        result = PointResp(point=user.point,sweetheart_point=sweetheart.point)
        return APIResult.success(data=result)
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


# 生成随机验证码函数
def generate_random_code(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))


# 邮件验证码生成接口
@router.post("/get_code", response_model=APIResult[str])
async def generate_code(
    email: EmailStr,  # 验证邮箱格式
    session: AsyncSession = Depends(get_db_session)
) -> APIResult[str]:
    # 查询数据库中是否已存在该邮箱的验证码
    try:
        verification = verificationCodeCRUD.get_code(session,email)
        if verification.expire_time > datetime.utcnow():
            
        return APIResult.success(verification.code)
    except Exception as e:

    if existing_code:
        # 验证码是否未过期
        if existing_code.expire_time > datetime.utcnow():
            raise HTTPException(status_code=400, detail="验证码已发送，请稍后再试")

        # 如果已过期，删除旧验证码
        await session.delete(existing_code)
        await session.commit()

    # 生成新的验证码
    code = generate_random_code()
    expire_time = datetime.utcnow() + timedelta(minutes=CODE_EXPIRATION_MINUTES)

    # 保存到数据库
    new_code = VerificationCode(email=email, code=code, expire_time=expire_time)
    session.add(new_code)
    await session.commit()

    # 发送验证码到用户邮箱（假设有实现了send_email函数）
    try:
        await send_email(email, "注册验证码", f"您的验证码是：{code}，有效期为{CODE_EXPIRATION_MINUTES}分钟")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"邮件发送失败: {str(e)}")

    return APIResult(success=True, data="验证码已发送，请检查邮箱")


# 注册请求的数据模型
class RegisterReq(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    code: str = Field(..., min_length=6, max_length=6)


# 用户注册接口
@router.post("/register", response_model=APIResult[str])
async def register(
    req: RegisterReq = Body(...),
    session: AsyncSession = Depends(get_db_session)
) -> APIResult[str]:
    # 验证验证码
    result = await session.execute(select(VerificationCode).where(VerificationCode.email == req.email, VerificationCode.code == req.code))
    code_entry = result.scalars().first()

    if not code_entry:
        raise HTTPException(status_code=400, detail="验证码无效")

    if code_entry.expire_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="验证码已过期")

    # 删除验证码（防止重复使用）
    await session.delete(code_entry)
    await session.commit()

    # 检查邮箱是否已注册
    result = await session.execute(select(User).where(User.email == req.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="该邮箱已注册")

    # 创建新用户
    new_user = User(
        email=req.email,
        hashed_password=hash_password(req.password),  # 假设有一个密码哈希函数
        created_at=datetime.utcnow()
    )
    session.add(new_user)
    await session.commit()

    return APIResult(success=True, data="注册成功")
'''