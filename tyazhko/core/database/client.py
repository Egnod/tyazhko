from motor import motor_asyncio

from tyazhko.core.config import configurator

__all__ = ["mongo_db", "mongo_client"]


class Mongo:
    _USER = configurator.get_config("database_user")
    _PASSWORD = configurator.get_config("database_password")
    _HOST = configurator.get_config("database_host")
    _PORT = configurator.get_config("database_port")
    _NAME = configurator.get_config("database_name")

    _MONGO_DATABASE_URI = f"mongodb://{_USER}:{_PASSWORD}@{_HOST}:{_PORT}"

    def __init__(self):
        self._client = motor_asyncio.AsyncIOMotorClient(
            self._MONGO_DATABASE_URI, connect=True, maxPoolSize=200
        )

        self._db = self._client[self._NAME]

    @property
    def db(self):
        return self._db

    @property
    def client(self):
        return self._client

    def close(self):
        self._client.close()


mongo_instanse = Mongo()
mongo_client = mongo_instanse.client
mongo_db = mongo_instanse.db
