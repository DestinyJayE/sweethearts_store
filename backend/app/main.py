# main.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .routers import router_goods
from .routers import router_user
from .routers import router_task
import asyncio
app = FastAPI()


origins = [
    "http://localhost:8081",
    "http://192.168.137.1:8081",
    "*",
]


# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许跨域请求的源列表
    allow_credentials=True,  # 允许凭据
    allow_methods=["*"],    # 允许跨域请求的HTTP方法列表
    allow_headers=["*"],    # 允许跨域请求的HTTP头部列表
)


app.include_router(router=router_goods, prefix="/api/goods", tags=["商品模块"])
app.include_router(router=router_task, prefix="/api/task", tags=["任务模块"])
app.include_router(router=router_user,prefix="/api/user", tags=["用户模块"])