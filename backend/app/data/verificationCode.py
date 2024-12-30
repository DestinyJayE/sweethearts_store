from pydantic import BaseModel, Field


class VerificationCode(BaseModel):
    id: int = Field(default=0, comment="主键")
    email: str = Field(default="", comment="邮箱")
    code: str = Field(default="", comment="验证码")
    expire_time: int = Field(default=0, comment="过期时间")

    class Config:
        from_attributes = True