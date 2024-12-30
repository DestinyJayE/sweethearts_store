from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


# 获取指定邮箱验证码
async def update_user_point(session: AsyncSession, user_id: int, point: int) -> VerificationCode: