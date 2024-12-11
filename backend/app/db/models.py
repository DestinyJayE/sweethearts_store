# db.models
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .base import Base


# 用户表
class UserInDB(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_name = Column(String(255), nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    email = Column(String(255), nullable=False, comment="邮箱")
    sweethearts_id = Column(Integer, default=0, comment="恋人ID")

    def __repr__(self):
        return f"<User(id={self.id}, user_name={self.user_name}, email={self.email})>"


# 商品表
class GoodsInDB(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    name = Column(String(255), nullable=False, comment="商品名称")
    price = Column(String(255), nullable=False, comment="价格")
    content = Column(String(255), nullable=False, comment="商品描述")
    create_id = Column(Integer, nullable=False, comment="创建者ID")
    num = Column(Integer, nullable=False, comment="库存数量")

    def __repr__(self):
        return f"<Goods(id={self.id}, name={self.name}, price={self.price})>"


# 卡券表
class CardsInDB(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    name = Column(String(255), nullable=False, comment="卡券名称")
    price = Column(String(255), nullable=False, comment="价格")
    content = Column(String(255), nullable=False, comment="卡券描述")
    haven_id = Column(Integer, nullable=False, comment="拥有者ID")
    num = Column(Integer, nullable=False, comment="库存数量")

    def __repr__(self):
        return f"<Cards(id={self.id}, name={self.name}, price={self.price})>"


# 任务表
class TaskInDB(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    name = Column(String(255), nullable=False, comment="任务名称")
    price = Column(String(255), nullable=False, comment="任务奖励")
    content = Column(String(255), nullable=False, comment="任务描述")
    create_id = Column(Integer, nullable=False, comment="创建者ID")
    is_finish = Column(Integer, default=0, comment="是否完成")

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, is_finish={self.is_finish})>"
