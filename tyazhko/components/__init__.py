from typing import List

from fastapi import APIRouter

from tyazhko.components import links
from tyazhko.components.links import COLLECTIONS as LINKS_COLLECTIONS

__all__ = ["COLLECTIONS", "get_components_router"]

COLLECTIONS: List[str] = [*LINKS_COLLECTIONS]


def get_components_router() -> APIRouter:
    router = APIRouter()

    router.include_router(links.router, prefix="", tags=["link"])

    return router
