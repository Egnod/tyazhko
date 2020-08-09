import secrets
from datetime import datetime
from typing import List, Type

from tyazhko.components.links.schemas import LinkRequest, LinkResponse
from tyazhko.core.database.crud import BaseMongoCRUD


class LinkCRUD(BaseMongoCRUD):
    collection = "links"

    @classmethod
    async def get_definitions_domain(cls, bytes_count: int):
        alphabet_count = 64
        return alphabet_count ** len(secrets.token_urlsafe(bytes_count))

    @classmethod
    async def generate_short_id(cls):
        short_id = None

        for bytes_count in range(1, 7):
            shorts_count = len(
                await cls.find_many(
                    {"short_id": {"$size": len(secrets.token_urlsafe(bytes_count))}}
                )
            )
            remain_definitions = (
                await cls.get_definitions_domain(bytes_count)
            ) - shorts_count

            if remain_definitions <= 0:
                continue

            short_id = secrets.token_urlsafe(bytes_count)
            found = await cls.find_one({"short_id": short_id})

            if not found:
                break

        return short_id

    @classmethod
    async def create(cls, data: LinkRequest, creator_info: dict = None) -> LinkResponse:
        data = data.dict()

        return (
            await cls.insert_one(
                {
                    "short_id": await cls.generate_short_id(),
                    "created_at": datetime.now(),
                    "creator_info": creator_info,
                    "getter_info": [],
                    **data,
                }
            )
        ).inserted_id


CRUDS: List[Type[BaseMongoCRUD]] = [LinkCRUD]
