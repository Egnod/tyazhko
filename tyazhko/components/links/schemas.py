from pydantic import Field, HttpUrl

from tyazhko.core.schemas import BaseSchema


class LinkRequest(BaseSchema):
    origin_link: HttpUrl = Field(...)


class LinkResponse(BaseSchema):
    short_id: str = Field(...)
    origin_link: HttpUrl = Field(...)
