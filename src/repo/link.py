from typing import List, Union, Dict, Any, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection as DBCollection

from src.repo.base import BaseRepo
from src.schemas.link import LinkInDB, LinkCreate, LinkUpdate


class LinkRepo(BaseRepo[LinkInDB, LinkCreate, LinkUpdate]):
    async def get_by_short_urn(
            self,
            collection: DBCollection,
            urn: str
    ) -> Optional[LinkInDB]:
        obj = await collection.find_one({'short_urn': urn})
        if not obj:
            return None
        obj['id'] = str(obj.pop('_id'))
        return self.model(**obj)

    @staticmethod
    async def can_be_created(
            collection: DBCollection,
            obj_in: LinkCreate
    ) -> tuple[bool, Optional[str]]:
        obj = await collection.find_one({'short_urn': obj_in.short_urn})
        if obj:
            return False, 'Short URN is not unique'
        return True, None

    async def create(
            self,
            collection: DBCollection,
            obj_in: Union[LinkCreate, Dict[str, Any]],
    ) -> LinkInDB:
        if not isinstance(obj_in, dict):
            obj_in = obj_in.dict(exclude_unset=True)
        return await super(LinkRepo, self).create(collection, obj_in=obj_in)

    async def create_with_owner_and_short_urn(
            self,
            collection: DBCollection,
            obj_in: LinkCreate,
            owner_id: str | ObjectId,
            short_urn: str
    ) -> LinkInDB:
        obj_in = obj_in.dict()
        obj_in['owner_id'] = str(owner_id)
        obj_in['short_urn'] = short_urn
        return await self.create(collection, obj_in=obj_in)

    async def get_multy_by_owner(
            self,
            collection: DBCollection,
            owner_id: str | ObjectId,
            skip: int = 0,
            limit: int = 10
    ) -> List[LinkInDB]:
        objs = await collection.find(
            {'owner_id': ObjectId(owner_id)},
            skip=skip
        ).to_list(length=limit)
        return [self.model(**obj) for obj in objs]


link = LinkRepo(LinkInDB)
