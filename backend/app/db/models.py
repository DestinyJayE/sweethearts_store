from sqlalchemy import Column, Integer, String

from .base import Base


class UserInDB(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    user_name = Column(String(255), nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    email = Column(String(255), nullable=False, comment="邮箱")
    point = Column(Integer, default=0, comment="积分")
    sweetheart_id = Column(Integer, default=0, comment="恋人ID")

    def __repr__(self):
        return f"<User(id={self.id}, user_name={self.user_name}, email={self.email})>"


class GoodsInDB(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    des = Column(String(255), nullable=False)
    create_id = Column(Integer, nullable=False)
    num = Column(Integer, nullable=False)
    is_deleted = Column(Integer, default=0, comment="0未删除 1删除")

    def __repr__(self):
        return f"<Goods(id={self.id}, name={self.name}, price={self.price})>"


class GoodsUserInDB(Base):
    __tablename__ = "goods_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    goods_id = Column(Integer, nullable=False)
    owner_id = Column(Integer, nullable=False)
    user_purchased_quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<GoodsUser(id={self.id}, goods_id={self.goods_id}, owner_id={self.owner_id})>"


class TaskInDB(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    des = Column(String(255), nullable=False)
    create_id = Column(Integer, nullable=False)
    is_finish = Column(Integer, default=0)

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, price={self.price})>"
