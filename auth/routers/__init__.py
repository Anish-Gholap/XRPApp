from fastapi import APIRouter


auth_router = APIRouter(prefix='/auth', tags=["Authentication"])

auth_router.include_router(, prefix="/")