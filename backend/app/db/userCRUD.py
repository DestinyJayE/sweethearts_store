# db.userCRUD.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import UserInDB
from app.data import User


# 为指定用户修改积分
async def update_user_point(session: AsyncSession, user_id: int, point: int) -> UserInDB:
    result = await session.execute(select(UserInDB).where(UserInDB.id == user_id))
    user = result.scalar_one()
    user.point = point
    await session.commit()
    await session.refresh(user)
    return user


# 获取指定用户信息
async def get_user_info(session: AsyncSession, user_id: int) -> UserInDB:
    result = await session.execute(select(UserInDB).where(UserInDB.id == user_id))
    return result.scalar_one()


async def get_all_user(session: AsyncSession, page_size: int, page_number: int) -> list:
    result = await session.execute(select(UserInDB).limit(page_size).offset(page_number - 1))
    return result.scalars().all()


async def add_user(session: AsyncSession, user: User) -> UserInDB:
    user_dict = user.dict(exclude={'id'})
    new_user = UserInDB(**user_dict)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def delete_user(session: AsyncSession, user_id: int) -> UserInDB:
    result = await session.execute(select(UserInDB).where(UserInDB.id == user_id))
    user = result.scalar_one()
    await session.delete(user)
    await session.commit()
    return user


async def get_user(session: AsyncSession, user_id: int) -> UserInDB:
    result = await session.execute(select(UserInDB).where(UserInDB.id == user_id))
    return result.scalar_one()


async def add_user_point(session: AsyncSession, user_id: int, point: int) -> UserInDB:
    result = await session.execute(select(UserInDB).where(UserInDB.id == user_id))
    user = result.scalar_one()
    user.point += point
    await session.commit()
    return user
