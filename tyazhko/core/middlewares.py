from fastapi import FastAPI
from fastapi.middleware import cors
from loguru import logger


def set_middlewares(app: FastAPI) -> FastAPI:
    logger.info("Set middlewares started")

    app.add_middleware(
        cors.CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origins=["*"],
    )

    logger.info("Set middlewares complete")
    return app
