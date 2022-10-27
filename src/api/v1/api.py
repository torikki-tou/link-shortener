from fastapi import APIRouter

from src.api.v1.endpoints import (
    users,
    links,
    auth
)


router = APIRouter()
router.include_router(
    router=users.router, prefix='/user', tags=['users'])
router.include_router(
    router=links.router, prefix='/links', tags=['links'])
router.include_router(
    router=auth.router, prefix='/auth', tags=['auth'])
