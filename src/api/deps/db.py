from functools import cached_property
from typing import Callable

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from motor.motor_asyncio import AsyncIOMotorCollection as DBCollection

from src.db.client import MongoClientGenerator


get_mongo_client = MongoClientGenerator()


class APICollections:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.__database = database

    @cached_property
    def users(self) -> Callable[[], DBCollection]:
        return lambda: self.__database.users

    @cached_property
    def links(self) -> Callable[[], DBCollection]:
        return lambda: self.__database.links


class Databases:

    def __init__(self):
        self.__client = get_mongo_client()

    @cached_property
    def api(self) -> APICollections:
        return APICollections(self.__client.api)


get_db_collection = Databases()
