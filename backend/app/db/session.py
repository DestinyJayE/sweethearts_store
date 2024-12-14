# db.session.py
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/sweethearts"  # 使用 aiomysql

# 创建引擎
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# 创建 session 工厂
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# 提供一个依赖，用于为每个请求创建和清理 session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
