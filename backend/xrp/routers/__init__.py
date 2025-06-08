from fastapi import APIRouter

from .loan_router import loan_router

xrp_router = APIRouter()
xrp_router.include_router(loan_router, prefix="/loan")
