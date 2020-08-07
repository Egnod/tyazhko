from http import HTTPStatus

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path
from starlette.responses import RedirectResponse

from tyazhko.components.links.crud import LinkCRUD
from tyazhko.components.links.schemas import LinkRequest, LinkResponse

router = APIRouter()


@router.post("/", response_model=LinkResponse)
async def create_link(schema: LinkRequest) -> LinkResponse:
    link = await LinkCRUD.find_one({"origin_link": schema.origin_link})

    if link:
        return link

    link_id = await LinkCRUD.create(schema)

    link = await LinkCRUD.find_one({"_id": ObjectId(link_id)})

    if not link:
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR)

    return LinkResponse(**link)


@router.get("/{short_id}", response_class=RedirectResponse)
async def get_link(short_id: str = Path(...)):
    link = await LinkCRUD.find_one({"short_id": short_id})

    if not link:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    return RedirectResponse(url=link["origin_link"])
