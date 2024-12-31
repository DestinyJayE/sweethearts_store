from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import VerificationCodeInDB
from app.data import VerificationCode

# 获取指定邮箱验证码
async def get_code(session: AsyncSession, email: str) -> VerificationCode:
    result = await session.execute(select(VerificationCodeInDB).where(VerificationCodeInDB.email == email))
    verification = result.scalar_one()
    return VerificationCode.from_orm(verification)


async def add_code(session: AsyncSession, verification: VerificationCode) -> VerificationCode:
    verification_dict = verification.dict(exclude={'id'})
    new_verification = VerificationCodeInDB(**verification_dict)
    session.add(new_verification)
    await session.flush()
    return VerificationCode.from_orm(new_verification)


async def delete_code(session: AsyncSession, email: str) -> VerificationCode:
    result = await session.execute(select(VerificationCodeInDB).where( VerificationCodeInDB.email == email))
    verification = result.scalar_one()
    await session.delete(verification)
    return VerificationCode.from_orm(verification)

