from fastapi import APIRouter
from auth.routers.did import did_router
from auth.routers.auth import authentication_router


auth_router = APIRouter()

auth_router.include_router(did_router, prefix="/did")
auth_router.include_router(authentication_router, prefix="/auth")