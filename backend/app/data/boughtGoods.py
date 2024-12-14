from pydantic import BaseModel, Field


class BoughtGoods(BaseModel):
    id: int = Field(default=0, title="主键")
    name: str = Field(default="", title="商品名称")
    price: int = Field(default=0, title="价格")
    des: str = Field(default="", title="商品描述")
    create_id: int = Field(default=0, title="创建者ID")
    num: int = Field(default=0, title="库存数量")
    user_purchased_quantity: int = Field(default=0, title="购买数量")
    is_deleted: int = Field(default=0, title="是否删除 0未删除 1删除")

    class Config:
        from_attributes = True
