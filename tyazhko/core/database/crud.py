import abc
from typing import Union

from bson import ObjectId
from passlib.hash import argon2

from tyazhko.core.database.client import mongo_db


class BaseMongoCRUD(abc.ABC):
    db = mongo_db
    collection = NotImplemented

    @classmethod
    async def find_by_id(cls, _id: Union[str, ObjectId], **kwargs):
        objs = cls.db[cls.collection].find(filter={"_id": ObjectId(_id)}, **kwargs)

        return next(iter([obj async for obj in objs]), None)

    @classmethod
    async def find_one(cls, query: dict):
        objs = cls.db[cls.collection].find(filter=query)

        return next(iter([obj async for obj in objs]), None)

    @classmethod
    async def find_many(cls, query: dict, options: dict = None, sort: list = None):
        items = cls.db[cls.collection].find(query, options)

        if sort:
            items.sort(sort)

        return [i async for i in items]

    @classmethod
    async def insert_one(cls, payload: dict, options: dict = None):
        return await cls.db[cls.collection].insert_one(payload, options)

    @classmethod
    async def insert_many(cls, payload: list, options: dict = None):
        return await cls.db[cls.collection].insert_many(payload, options)

    @classmethod
    async def update_one(
        cls, query: dict, payload: dict, with_set_option: bool = True, **kwargs
    ):
        payload = {"$set": payload} if with_set_option else payload
        return await cls.db[cls.collection].update_one(query, payload, **kwargs)

    @classmethod
    async def update_many(
        cls, query: dict, payload: dict, with_set_option: bool = True, **kwargs
    ):
        payload = {"$set": payload} if with_set_option else payload
        return [
            i
            async for i in cls.db[cls.collection].update_many(query, payload, **kwargs)
        ]

    @classmethod
    async def delete_one(cls, query: dict, **kwargs):
        return await cls.db[cls.collection].delete_one(query, **kwargs)

    @classmethod
    async def delete_many(cls, query: dict, **kwargs):
        return await cls.db[cls.collection].delete_many(query, **kwargs)

    @classmethod
    async def aggregate(cls, pipeline: list, **kwargs):
        return [i async for i in cls.db[cls.collection].aggregate(pipeline, **kwargs)]

    @classmethod
    async def check_hash(cls, secret_hash: str, secret: str) -> bool:
        return argon2.verify(secret, secret_hash)

    @classmethod
    async def get_secret_hash(cls, secret: str) -> str:
        return argon2.hash(secret)
