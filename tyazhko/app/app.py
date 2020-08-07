from fastapi import FastAPI
from loguru import logger

from tyazhko import __project__, __version__
from tyazhko.core.database.utils import (
    auto_populate_collections,
    close_db_connect,
    open_db_connect,
)
from tyazhko.core.exceptions_handlers import set_exceptions_handlers
from tyazhko.core.logging import set_logging
from tyazhko.core.middlewares import set_middlewares
from tyazhko.core.routers import set_routers


def create_app() -> FastAPI:
    logger.info("Start create app object")

    app = FastAPI(
        title=__project__,
        version=__version__,
        on_startup=[open_db_connect, auto_populate_collections],
        on_shutdown=[close_db_connect],
        docs_url="/api/docs",
        redoc_url=None,
    )

    app = set_middlewares(app)
    app = set_routers(app)
    app = set_exceptions_handlers(app)

    set_logging()

    logger.info("Complete create app object")
    return app
