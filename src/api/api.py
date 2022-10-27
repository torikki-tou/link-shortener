from fastapi import APIRouter

from src.api.v1 import api as api_v1


api_router = APIRouter()
api_router.include_router(router=api_v1.router, prefix='/v1')
