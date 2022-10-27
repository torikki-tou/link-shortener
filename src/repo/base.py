from typing import TypeVar, Generic, Union, Dict, Any, Type, Optional

from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection as DBCollection

ModelInDB = TypeVar('ModelInDB', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class BaseRepo(Generic[ModelInDB, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[ModelInDB]):
        self.model = model

    async def get(
            self,
            collection: DBCollection,
            id_: str | ObjectId
    ) -> Optional[ModelInDB]:
        if not isinstance(id_, ObjectId) and not ObjectId.is_valid(id_):
            return None
        obj = await collection.find_one({'_id': ObjectId(id_)})
        if not obj:
            return None
        obj['id'] = str(obj.pop('_id'))
        return self.model(**obj)

    async def create(
            self,
            collection: DBCollection,
            obj_in: Union[CreateSchema, Dict[str, Any]]
    ) -> ModelInDB:
        if not isinstance(obj_in, dict):
            obj_in = obj_in.dict(exclude_unset=True)
        obj_id = (await collection.insert_one(obj_in)).inserted_id
        return await self.get(collection, id_=obj_id)

    async def update(
            self,
            collection: DBCollection,
            id_: str | ObjectId,
            obj_in: Union[UpdateSchema, Dict[str, Any]]
    ) -> Optional[ModelInDB]:
        if not isinstance(id_, ObjectId) and not ObjectId.is_valid(id_):
            return None
        if not isinstance(obj_in, dict):
            obj_in = obj_in.dict(exclude_unset=True)
        await collection.update_one({'_id': ObjectId(id_)}, {'$set': obj_in})
        return await self.get(collection, id_=id_)

    async def remove(
            self,
            collection: DBCollection,
            id_: str | ObjectId
    ) -> Optional[ModelInDB]:
        if not isinstance(id_, ObjectId) and not ObjectId.is_valid(id_):
            return None
        obj = await self.get(collection, id_=id_)
        if not obj:
            return None
        await collection.delete_one({'_id': ObjectId(id_)})
        return self.model(**obj.dict())
