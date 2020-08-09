from datetime import datetime
from http import HTTPStatus

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path
from starlette.requests import Request
from starlette.responses import RedirectResponse

from tyazhko.components.links.crud import LinkCRUD
from tyazhko.components.links.schemas import LinkRequest, LinkResponse

router = APIRouter()


@router.post("/", response_model=LinkResponse)
async def create_link(request: Request, schema: LinkRequest) -> LinkResponse:
    link = await LinkCRUD.find_one({"origin_link": schema.origin_link})

    if link:
        return link

    creator_info = {
        "data": await request.json(),
        "headers": dict(request.headers),
        "cookies": dict(request.cookies),
        "host": dict(request.client._asdict()),
    }

    link_id = await LinkCRUD.create(schema, creator_info=creator_info)

    link = await LinkCRUD.find_one({"_id": ObjectId(link_id)})

    if not link:
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR)

    return LinkResponse(**link)


@router.get("/{short_id}", response_class=RedirectResponse)
async def get_link(request: Request, short_id: str = Path(...)):
    link = await LinkCRUD.find_one({"short_id": short_id})

    if not link:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    getter_info = {
        "headers": dict(request.headers),
        "cookies": dict(request.cookies),
        "host": dict(request.client._asdict()),
    }

    link["getter_info"].append(getter_info)
    await LinkCRUD.update_one(
        {"short_id": short_id},
        {"last_getted_at": datetime.now(), "getter_info": link["getter_info"]},
    )

    return RedirectResponse(url=link["origin_link"])
