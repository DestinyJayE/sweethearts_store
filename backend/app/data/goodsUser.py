from pydantic import BaseModel, Field


class GoodsUser(BaseModel):
    id: int = Field(default=0, comment="主键")
    goods_id: int = Field(default=0, nullable=False, comment="商品ID")
    owner_id: int = Field(default=0, nullable=False, comment="所有者ID")
    user_purchased_quantity: int = Field(default=0, nullable=False, comment="数量")

    class Config:
        from_attributes = True