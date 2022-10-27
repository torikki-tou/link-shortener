from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorCollection as DBCollection

from src import schemas, repo
from src.core import security
from src.api import deps


router = APIRouter()


@router.post(
    '/sign_up',
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
async def sign_up(
        name: str = Form(),
        username: str = Form(),
        password: str = Form(),
        db_collection: DBCollection = Depends(deps.get_db_collection.api.users)
):
    obj_in = schemas.UserCreate(
        name=name, email=username, password=password)
    can_be, reason = await repo.user.can_be_created(
        db_collection, obj_in=obj_in
    )
    if not can_be:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=reason
        )
    user = await repo.user.create(db_collection, obj_in=obj_in)
    return schemas.User(**user.dict())


@router.post(
    '/token',
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK
)
async def get_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db_collection: DBCollection = Depends(deps.get_db_collection.api.users)
):
    user = await repo.user.authenticate(
        db_collection,
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return schemas.Token(
        access_token=security.create_access_token(user.id)
    )
