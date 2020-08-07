from fastapi import APIRouter, FastAPI
from loguru import logger


def set_routers(app: FastAPI) -> FastAPI:
    logger.info("Start collecting routers")

    from tyazhko.components import get_components_router

    api_router = APIRouter()

    api_router.include_router(get_components_router())
    app.include_router(api_router)

    logger.info("Complete collecting routers")

    return app
