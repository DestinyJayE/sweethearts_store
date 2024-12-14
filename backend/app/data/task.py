from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int = Field(default=0, comment="主键")
    name: str = Field(default="", comment="任务名称")
    price: int = Field(default=0, comment="任务奖励")
    des: str = Field(default="", comment="任务描述")
    create_id: int = Field(default=0, comment="创建者ID")
    is_finish: int = Field(default=0, comment="是否完成")

    class Config:
        from_attributes = True
