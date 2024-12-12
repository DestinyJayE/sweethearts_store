# db.crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import UserInDB,GoodsInDB


async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(select(UserInDB).where(UserInDB.id == user_id))
    return result.scalars().first()


async def create_user(session: AsyncSession, name: str, email: str, password: str):
    new_user = UserInDB(user_name=name, email=email, password=password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


