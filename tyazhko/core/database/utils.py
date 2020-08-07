from loguru import logger

from tyazhko.components import COLLECTIONS
from tyazhko.core.database.client import mongo_client, mongo_db


async def open_db_connect():
    logger.info("Starting prepopulate db")
    is_failed = None

    try:
        await mongo_client.admin.command("ping")
    except Exception as e:
        is_failed = True
        logger.error(f"Unable to connect DB, error {e.__class__.__name__}")

    if not is_failed:
        logger.info("Successfully open db connect")

    else:
        exit(-1)


async def close_db_connect():
    logger.info("Close DB connect")


async def auto_populate_collections():
    logger.info("Start auto populate not exists collections")

    exist_collections = await mongo_db.list_collection_names()

    for collection in COLLECTIONS:
        if collection not in exist_collections:
            logger.info("{} not exist", collection)

            await mongo_db.create_collection(collection)

            logger.info("{} populated", collection)

    logger.info("End auto populate not exists collections")
