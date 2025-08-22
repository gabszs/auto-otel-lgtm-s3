from fastapi import APIRouter

from .password_routes import router

routers = APIRouter(prefix="/v1")
routers.include_router(router)

__all__ = ["routers"]
