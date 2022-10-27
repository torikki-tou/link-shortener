from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection as DBCollection

from src import schemas, repo
from src.api import deps
from src import links

router = APIRouter()


@router.get(
    '/{link_id}',
    response_model=schemas.Link,
    status_code=status.HTTP_200_OK
)
async def read_link(
        link_id: str,
        current_user: schemas.UserInDB = Depends(deps.get_current_user),
        db_collection: DBCollection = Depends(deps.get_db_collection.api.links)
):
    if not(current_user.id == link_id or current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    link = await repo.link.get(db_collection, id_=link_id)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return schemas.Link(**link.dict())


@router.post(
    '/',
    response_model=schemas.Link,
    status_code=status.HTTP_201_CREATED
)
async def create_link(
        obj_in: schemas.LinkCreate,
        current_user: schemas.UserInDB = Depends(deps.get_current_user),
        db_collection: DBCollection = Depends(deps.get_db_collection.api.links)
):
    for _ in range(5):
        short_urn = links.make.short_urn(obj_in.uri)
        if not await repo.link.get_by_short_urn(db_collection, urn=short_urn):
            break
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    link = await repo.link.create_with_owner_and_short_urn(
        db_collection,
        obj_in=obj_in,
        owner_id=current_user.id,
        short_urn=short_urn
    )
    return schemas.Link(**link.dict())


@router.patch(
    '/{link_id}',
    response_model=schemas.Link,
    status_code=status.HTTP_200_OK
)
async def update_link(
        link_id: str,
        obj_in: schemas.LinkUpdate,
        current_user: schemas.UserInDB = Depends(deps.get_current_user),
        db_collection: DBCollection = Depends(deps.get_db_collection.api.links)
):
    if not(current_user.id == link_id or current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    link = await repo.link.update(db_collection, id_=link_id, obj_in=obj_in)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return schemas.Link(**link.dict())


@router.delete(
    '/{link_id}',
    response_model=schemas.Link,
    status_code=status.HTTP_200_OK
)
async def remove_link(
        link_id: str,
        current_user: schemas.UserInDB = Depends(deps.get_current_user),
        db_collection: DBCollection = Depends(deps.get_db_collection.api.links)
):
    if not(current_user.id == link_id or current_user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    link = await repo.link.remove(db_collection, id_=link_id)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return schemas.Link(**link.dict())
