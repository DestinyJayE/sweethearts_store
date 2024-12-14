from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

# 定义泛型类型变量
T = TypeVar("T")


# 泛型 APIResult 类
class APIResult(BaseModel, Generic[T]):
    code: str  # 状态码
    msg: str  # 消息
    data: Optional[T] = None  # 数据部分，可以是任意类型

    @staticmethod
    def success(data: Optional[T] = None, msg: str = "Success") -> "APIResult[T]":
        """快速构造成功的返回值"""
        return APIResult(code="200", msg=msg, data=data)

    @staticmethod
    def error(code: str = "500", msg: str = "Error") -> "APIResult[T]":
        """快速构造失败的返回值"""
        return APIResult(code=code, msg=msg, data=None)
