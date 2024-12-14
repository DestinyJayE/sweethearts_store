# main.py

from fastapi import FastAPI

from .routers import router_goods
from .routers import router_user
from .routers import router_task
app = FastAPI()

app.include_router(router=router_goods, prefix="/api/goods", tags=["商品模块"])
app.include_router(router=router_task, prefix="/api/task", tags=["任务模块"])
app.include_router(router=router_user,prefix="/api/user", tags=["用户模块"])