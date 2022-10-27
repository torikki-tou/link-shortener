from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorCollection as DBCollection

from src import repo
from src.api import deps


router = APIRouter()


@router.get(
    '/{short_urn}',
    response_class=RedirectResponse,
)
async def redirect(
        short_urn: str,
        db_collection: DBCollection = Depends(deps.get_db_collection.api.links)
):
    link = await repo.link.get_by_short_urn(db_collection, urn=short_urn)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(link.uri)
