# routers.user.py
import pydantic
from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.data import APIResult, Goods, BoughtGoods
from app.db import get_db_session, goodsCRUD, userCRUD, goodsUserCRUD
from app.util import get_user_id_from_token

router = APIRouter()


@router.get("/self_goods", response_model=APIResult[list[Goods]])
async def get_goods(
        page_number: int = 1,
        page_size: int = 10,
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session)
) -> APIResult[list[Goods]]:
    try:
        goods_list = await goodsCRUD.get_creator_goods(session, user_id=user_id, page_size=page_size,
                                                       page_number=page_number)
        return APIResult.success(data=goods_list)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.get("/sweetheart_goods", response_model=APIResult[list[Goods]])
async def get_sweetheart_goods(
        page_number: int = 1,
        page_size: int = 10,
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session)
) -> APIResult[list[Goods]]:
    try:
        user = await userCRUD.get_user(session, user_id)
        goods_list = await goodsCRUD.get_creator_goods(session, user_id=user.sweetheart_id, page_size=page_size,
                                                       page_number=page_number)
        return APIResult.success(data=goods_list)
    except Exception as e:
        return APIResult.error(msg=str(e))


class AddGoodsReq(BaseModel):
    name: str = pydantic.Field(description="商品名称")
    des: str = pydantic.Field(description="商品描述")
    price: int = pydantic.Field(description="商品价格")
    num: int = pydantic.Field(description="商品数量")


@router.post("/add", response_model=APIResult[Goods])
async def add_goods(
        session: AsyncSession = Depends(get_db_session),
        user_id: int = Depends(get_user_id_from_token),
        req: AddGoodsReq = Body()
) -> APIResult[Goods]:
    try:
        add_dict = req.dict()
        add_dict["create_id"] = user_id
        _goods = Goods(**add_dict)
        async with session.begin():
            new_goods = await goodsCRUD.add_goods(session, _goods)
        return APIResult.success(data=new_goods)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.post("/delete", response_model=APIResult[Goods])
async def delete_goods(
        id: int,
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session),
) -> APIResult[Goods]:
    try:
        async with session.begin():
            deleted_goods = await goodsCRUD.delete_goods(session, id)
        return APIResult.success(data=deleted_goods)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.post("/buy", response_model=APIResult[Goods])
async def buy_goods(
        id: int,
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session),
) -> APIResult[Goods]:
    try:
        async with session.begin():
            goods = await goodsCRUD.get_goods_by_id(session, id)
            if goods.num <= 0:
                return APIResult.error(msg="商品数量不足", code="429")
            user = await userCRUD.get_user(session, user_id)
            if user.point < goods.price:
                return APIResult.error(msg="积分不足", code="429")
            goods = await goodsCRUD.set_goods_num(session, id, goods.num - 1)
            await userCRUD.update_user_point(session, user_id, user.point - goods.price)
            await goodsUserCRUD.add_goods_user(session, goods_id=id, user_id=user_id)
        return APIResult.success(data=goods)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.post("/set_goods_num", response_model=APIResult[Goods])
async def add_goods_num(
        id: int,
        num: int,
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session),
) -> APIResult[Goods]:
    try:
        async with session.begin():
            goods = await goodsCRUD.set_goods_num(session, goods_id=id, num=num)
        return APIResult.success(goods)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.get("/get_bought_goods", response_model=APIResult[list[BoughtGoods]])
async def get_bought_goods(
        page_number: int = 1,
        page_size: int = 10,
        user_id: int = Depends(get_user_id_from_token),
        session: AsyncSession = Depends(get_db_session)
) -> APIResult[list[BoughtGoods]]:
    try:
        bought_list = await goodsCRUD.get_bought_goods(session, user_id=user_id, page_size=page_size,
                                                       page_number=page_number)
        return APIResult.success(data=bought_list)
    except Exception as e:
        return APIResult.error(msg=str(e))
