from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(default=0, comment="主键")
    user_name: str = Field(default="", nullable=False, comment="用户名")
    password: str = Field(default="", nullable=False, comment="密码")
    email: str = Field(default="", nullable=False, comment="邮箱")
    point: int = Field(default=0, comment="积分")
    sweetheart_id: int = Field(default=0, comment="恋人ID")

    class Config:
        from_attributes = True