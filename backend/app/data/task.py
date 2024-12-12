from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int = Field(default=0, comment="主键")
    name: str = Field(default="", nullable=False, comment="任务名称")
    price: int = Field(default=0, nullable=False, comment="任务奖励")
    des: str = Field(default="", nullable=False, comment="任务描述")
    create_id: int = Field(default=0, nullable=False, comment="创建者ID")
    is_finish: int = Field(default=0, comment="是否完成")
    sweetheart_id: int = Field(default=0, comment="恋人ID")

    class Config:
        from_attributes = True