# db.goodsCRUD.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.data import Goods, BoughtGoods
from app.db.models import GoodsInDB, GoodsUserInDB


# 获取某人创建的所有商品
async def get_creator_goods(session: AsyncSession, page_size: int, page_number: int, user_id: int) -> list[Goods]:
    result = await session.execute(
        select(GoodsInDB).limit(page_size).offset(page_number - 1).where(GoodsInDB.create_id == user_id,
                                                                         GoodsInDB.is_deleted == 0))
    _goods = result.scalars().all()
    goods_list = []
    for item in _goods:
        goods_list.append(Goods.from_orm(item))
    return goods_list


# 添加商品
async def add_goods(session: AsyncSession, goods: Goods) -> Goods:
    goods_dict = goods.dict(exclude={'id'})
    new_goods = GoodsInDB(**goods_dict)
    session.add(new_goods)
    await session.flush()
    return Goods.from_orm(new_goods)


# 删除商品
async def delete_goods(session: AsyncSession, goods_id: int) -> Goods:
    result = await session.execute(select(GoodsInDB).where(GoodsInDB.id == goods_id))
    goods = result.scalar_one()
    goods.is_deleted = 1
    await session.flush()
    return Goods.from_orm(goods)


# 设置商品数量
async def set_goods_num(session: AsyncSession, goods_id: int, num: int) -> Goods:
    result = await session.execute(select(GoodsInDB).where(GoodsInDB.id == goods_id))
    goods = result.scalar_one()
    goods.num = num
    await session.flush()
    return Goods.from_orm(goods)


# 获取商品详情
async def get_goods_by_id(session: AsyncSession, goods_id: int) -> Goods:
    result = await session.execute(select(GoodsInDB).where(GoodsInDB.id == goods_id))
    goods = result.scalar_one()
    return Goods.from_orm(goods)


# 获取某人已经购买的所有商品
async def get_bought_goods(session: AsyncSession, page_size: int, page_number: int, user_id: int) -> list[BoughtGoods]:
    offset = (page_number - 1) * page_size
    # 查询返回 GoodsInDB 和 user_purchased_quantity
    query = (
        select(GoodsInDB, GoodsUserInDB.user_purchased_quantity)
        .join(GoodsUserInDB, GoodsInDB.id == GoodsUserInDB.goods_id)
        .where(GoodsUserInDB.owner_id == user_id)
        .limit(page_size)
        .offset(offset)
    )
    result = await session.execute(query)
    temp_goods = result.all()
    bought_list = []
    for goods, user_purchased_quantity in temp_goods:
        # 将 GoodsInDB 的数据和 user_purchased_quantity 合并到 BoughtGoods 中
        bought_item = BoughtGoods.from_orm(goods)
        bought_item.user_purchased_quantity = user_purchased_quantity
        bought_list.append(bought_item)
    return bought_list
