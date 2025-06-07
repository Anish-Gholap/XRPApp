from fastapi import APIRouter

from .general.routers import general_router

api_router = APIRouter()
api_router.include_router(general_router, prefix="/general")