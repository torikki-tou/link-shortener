from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection as DBCollection

from src.repo.base import BaseRepo
from src.schemas.user import UserInDB, UserCreate, UserUpdate
from src.core import security


class UserRepo(BaseRepo[UserInDB, UserCreate, UserUpdate]):
    async def create(
            self,
            collection: DBCollection,
            obj_in: UserCreate
    ) -> UserInDB:
        obj = obj_in.dict()
        obj['hashed_password'] = security.get_hashed_password(obj_in.password)
        del obj['password']
        return await super(UserRepo, self).create(collection, obj_in=obj)

    async def can_be_created(
            self,
            collection: DBCollection,
            obj_in: UserCreate
    ) -> tuple[bool, Optional[str]]:
        obj = await self.get_by_email(collection, email=obj_in.email)
        if obj:
            return False, 'Email already in use'
        return True, None

    async def update(
            self,
            collection: DBCollection,
            id_: str | ObjectId,
            obj_in: UserUpdate
    ) -> UserInDB:
        obj = obj_in.dict(exclude_unset=True)
        if 'password' in obj:
            obj['hashed_password'] = security.get_hashed_password(
                obj.pop('password')
            )
        return await super(UserRepo, self).update(
            collection,
            id_=id_,
            obj_in=obj
        )

    async def get_by_email(
            self,
            collection: DBCollection,
            email: str
    ) -> Optional[UserInDB]:
        obj = await collection.find_one({'email': email})
        if not obj:
            return None
        obj['id'] = str(obj.pop('_id'))
        return self.model(**obj)

    async def authenticate(
            self,
            collection: DBCollection,
            username: str,
            password: str
    ) -> Optional[UserInDB]:
        obj = await self.get_by_email(collection, email=username)
        if not obj:
            return None
        if not security.verify_password(password, obj.hashed_password):
            return None
        return obj


user = UserRepo(UserInDB)
