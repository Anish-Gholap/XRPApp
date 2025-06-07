from fastapi import APIRouter
from auth.routers.did import did_router


auth_router = APIRouter()

auth_router.include_router(did_router, prefix="/auth")