from pydantic import BaseModel, Field


class Goods(BaseModel):
    id: int = Field(default=0, comment="主键")
    name: str = Field(default="", comment="商品名称")
    price: int = Field(default=0, comment="价格")
    des: str = Field(default="", comment="商品描述")
    create_id: int = Field(default=0, comment="创建者ID")
    num: int = Field(default=0, comment="库存数量")
    is_deleted: int = Field(default=0, comment="是否删除 0未删除 1删除")

    class Config:
        from_attributes = True  # 允许通过orm模型实例化
