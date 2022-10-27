from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorCollection as DBCollection

from src import schemas, repo
from src.core import security
from src.api import deps


oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl=f"api/v1/auth/token"
)


async def get_current_user(
        token: str = Depends(oauth2_bearer),
        db_collection: DBCollection = Depends(deps.get_db_collection.api.users)
) -> schemas.UserInDB:
    user_id = security.get_user_id_from_access_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await repo.user.get(db_collection, id_=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
