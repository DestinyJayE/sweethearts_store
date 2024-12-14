from .goods import router as router_goods
from .user import router as router_user
from .task import router as router_task
__all__ = [
    "router_goods",
    "router_user",
    "router_task",
]