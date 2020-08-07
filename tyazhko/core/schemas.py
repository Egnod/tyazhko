import ujson
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        json_loads = ujson.loads
        json_dumps = ujson.dumps
