from fastapi import APIRouter
from xrp.routers import xrp_router

from .general import general_router

api_router = APIRouter()
api_router.include_router(general_router, prefix="/general")
api_router.include_router(xrp_router, prefix="/xrp")
