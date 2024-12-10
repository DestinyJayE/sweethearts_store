# main.py

from fastapi import FastAPI

from .routers import router_goods

app = FastAPI()



app.include_router(router=router_goods,prefix="/api/goods",tags=["商品模块"])