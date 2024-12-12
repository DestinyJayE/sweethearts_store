from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.data import GoodsUser
from app.db.models import GoodsUserInDB


async def add_goods_user(session: AsyncSession, user_id: int, goods_id: int) -> GoodsUser:
    result = await session.execute(
        select(GoodsUserInDB).where(GoodsUserInDB.owner_id == user_id, GoodsUserInDB.goods_id == goods_id))
    goods_user_in_db = result.scalar_one_or_none()
    if goods_user_in_db is None:
        goods_user_in_db = GoodsUserInDB(owner_id=user_id, goods_id=goods_id, user_purchased_quantity=1)
        session.add(goods_user_in_db)
        await session.commit()
        await session.refresh(goods_user_in_db)
        return GoodsUser.from_orm(goods_user_in_db)
    else:
        goods_user_in_db.user_purchased_quantity += 1
        await session.commit()
        await session.refresh(goods_user_in_db)
        return GoodsUser.from_orm(goods_user_in_db)
