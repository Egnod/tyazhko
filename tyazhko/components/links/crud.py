import secrets
from datetime import datetime
from typing import List, Type

from tyazhko.components.links.schemas import LinkRequest, LinkResponse
from tyazhko.core.database.crud import BaseMongoCRUD


class LinkCRUD(BaseMongoCRUD):
    collection = "links"

    @classmethod
    async def generate_short_id(cls):
        short_id = None

        while True:
            short_id = secrets.token_urlsafe(4)
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
