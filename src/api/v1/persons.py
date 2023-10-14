from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from src.models.person import Person
from src.api.v1.output_schemas.schema_persons import PersonListOut
from src.models.paginator import Paginator, get_paginator_params
from src.services.person_service import PersonService, get_person_service
from src.core.config import settings

router = APIRouter()


@router.get(
    "/",
    response_model=list[PersonListOut],
    summary="Person list",
    response_description="Get a list of all persons.",
)
@cache(expire=60 * settings.CACHE_EXPIRATION)
async def persons_list(
    paginator: Paginator = Depends(get_paginator_params),
    service: PersonService = Depends(get_person_service),
) -> list[PersonListOut]:
    persons, page_qty = await service.get_all(
        size=paginator.page_size,
        page_number=paginator.page_number,
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
        )
    return [PersonListOut(id=person.id, full_name=person.full_name) for person in persons]


@router.get(
    "/search",
    response_model=list[PersonListOut],
    summary="Person search results",
    response_description="Persons search results.",
)
@cache(expire=60 * settings.CACHE_EXPIRATION)
async def persons_search(
    query: str | None = None,
    paginator: Paginator = Depends(get_paginator_params),
    service: PersonService = Depends(get_person_service),
) -> list[PersonListOut]:
    query_dict = {
        "simple_query_string": {
            "query": query,
        }
    }
    persons, page_qty = await service.search_objects(
        query=query_dict,
        size=paginator.page_size,
        page_number=paginator.page_number,
    )
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
        )
    return [PersonListOut(id=person.id, full_name=person.full_name) for person in persons]


@router.get(
    "/{person_uuid}",
    response_model=Person,
    summary="Person data",
    response_description="Get info about the person with id, full_name and films.",
)
@cache(expire=60 * settings.CACHE_EXPIRATION)
async def person(
    person_uuid: UUID,
    service: PersonService = Depends(get_person_service),
) -> Person:
    data = await service.get_by_id(person_uuid)
    if not data:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
        )
    return data
