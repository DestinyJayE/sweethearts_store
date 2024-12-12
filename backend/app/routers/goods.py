# routers.user.py
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.data import APIResult, Goods
from app.db import get_db_session, goodsCRUD, userCRUD, goodsUserCRUD

router = APIRouter()


@router.get("/self_goods", response_model=APIResult[list])
async def get_goods(
        user_id: int,
        page_number: int = 1,
        page_size: int = 10,
        session: AsyncSession = Depends(get_db_session)
):
    try:
        goods_list = await goodsCRUD.get_creator_goods(session, user_id=user_id, page_size=page_size,
                                                       page_number=page_number)
        return APIResult.success(data=goods_list)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.get("/sweetheart_goods", response_model=APIResult[list])
async def get_sweetheart_goods(
        user_id: int,
        page_number: int = 1,
        page_size: int = 10,
        session: AsyncSession = Depends(get_db_session)
):
    try:
        user = await userCRUD.get_user(session, user_id)
        goods_list = await goodsCRUD.get_creator_goods(session, user_id=user.sweetheart_id, page_size=page_size,
                                                       page_number=page_number)
        return APIResult.success(data=goods_list)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.post("/add", response_model=APIResult[Goods])
async def add_goods(
        session: AsyncSession = Depends(get_db_session),
        req: Goods = Body()
):
    try:
        new_goods = await goodsCRUD.add_goods(session, req)
        return APIResult.success(data=new_goods)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.post("/delete", response_model=APIResult[Goods])
async def delete_goods(
        id: int,
        session: AsyncSession = Depends(get_db_session),
):
    try:
        deleted_goods = await goodsCRUD.delete_goods(session, id)
        return APIResult.success(data=deleted_goods)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.post("/buy", response_model=APIResult[Goods])
async def buy_goods(
        goods_id: int,
        user_id: int,
        session: AsyncSession = Depends(get_db_session),
):
    try:
        goods = await goodsCRUD.get_goods_by_id(session, goods_id)
        if goods.num <= 0:
            return APIResult.error(msg="商品数量不足",code="429")
        user = await userCRUD.get_user(session, user_id)
        if user.point < goods.price:
            return APIResult.error(msg="积分不足",code="429")
        goods = await goodsCRUD.set_goods_num(session, goods_id, goods.num - 1)
        await userCRUD.update_user_point(session, user_id, user.point - goods.price)
        await goodsUserCRUD.add_goods_user(session, goods_id=goods_id, user_id=user_id)
        return APIResult.success(data=goods)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.post("/add_goods_num", response_model=APIResult[Goods])
async def add_goods_num(
        goods_id: int,
        num: int,
        session: AsyncSession = Depends(get_db_session),
):
    try:
        goods = await goodsCRUD.get_goods_by_id(session, goods_id)
        goods = await goodsCRUD.set_goods_num(session, goods_id, goods.num + num)
        return APIResult.success(goods)
    except Exception as e:
        return APIResult.error(msg=str(e))


@router.get("/get_bought_goods", response_model=APIResult[list])
async def get_bought_goods(
        user_id: int,
        page_number: int = 1,
        page_size: int = 10,
        session: AsyncSession = Depends(get_db_session)
):
    try:
        bought_list = await goodsCRUD.get_bought_goods(session, user_id=user_id, page_size=page_size,
                                                       page_number=page_number)
        return APIResult.success(data=bought_list)
    except Exception as e:
        return APIResult.error(msg=str(e))
