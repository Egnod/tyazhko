import abc
from typing import Any, List, Optional, Union

import cbor2
from bson import ObjectId
from cryptography.fernet import Fernet
from passlib.hash import argon2

from tyazhko.core.database.client import mongo_db
from tyazhko.core.exceptions import GnosisCryptoKeyError


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
    def get_crypto_context(cls, key: bytes) -> Fernet:
        try:
            return Fernet(key)
        except Exception:
            raise GnosisCryptoKeyError()

    @classmethod
    def encrypt_fields(
        cls, data: dict, key: Optional[str], fields: Optional[List[str]] = None
    ) -> dict:
        data = data.copy()
        fields = fields if fields is not None else data.keys()

        for field in fields:
            data[field] = (
                cls.encrypt_data(key, data.get(field)) if key else data.get(field)
            )

        return data

    @classmethod
    def decrypt_fields(
        cls, data: dict, key: Optional[str], fields: Optional[List[str]]
    ) -> dict:
        data = data.copy()
        fields = fields if fields is not None else data.keys()

        for field in fields:
            data[field] = (
                cls.decrypt_data(key, data.get(field)) if key else data.get(field)
            )

        return data

    @classmethod
    def encrypt_data(cls, key: str, data: Any) -> bytes:
        data = cbor2.dumps(data)

        try:
            crypto_context = cls.get_crypto_context(key.encode())

            return crypto_context.encrypt(data)
        except Exception:
            raise GnosisCryptoKeyError()

    @classmethod
    def decrypt_data(cls, key: str, encrypted_data: bytes) -> Any:
        try:
            crypto_context = cls.get_crypto_context(key.encode())

            data = crypto_context.decrypt(encrypted_data)
        except Exception:
            raise GnosisCryptoKeyError()

        return cbor2.loads(data)

    @classmethod
    async def check_hash(cls, secret_hash: str, secret: str) -> bool:
        return argon2.verify(secret, secret_hash)

    @classmethod
    async def get_secret_hash(cls, secret: str) -> str:
        return argon2.hash(secret)
