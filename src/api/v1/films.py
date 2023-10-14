from http import HTTPStatus
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.models.film import Film
from src.api.v1.output_schemas.schema_films import FilmListOut
from src.models.paginator import Paginator, get_paginator_params
from src.services.film_service import FilmService, get_film_service
from src.core.config import settings
from src.services.genre_service import get_genre_service, GenreServie

router = APIRouter()


@router.get(
    "/",
    response_model=list[FilmListOut],
    summary="Film list",
    response_description="Get a list of all films.",
)
@cache(expire=60 * settings.CACHE_EXPIRATION)
async def films_list(
    paginator: Paginator = Depends(get_paginator_params),
    service: FilmService = Depends(get_film_service),
    genre_service: GenreServie = Depends(get_genre_service),
    sort_field: Optional[str] = None,
    genre_uuid: Optional[str] = None,
) -> list[FilmListOut]:
    # Получим имя жанра по его uuid
    genre_name = None
    if genre_uuid:
        genre_name = await genre_service.get_by_id(genre_uuid)
        genre_name = genre_name.name

    films, page_qty = await service.get_all(
        size=paginator.page_size,
        page_number=paginator.page_number,
        sort=sort_field,
        genre_name=genre_name,
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return [
        FilmListOut(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        )
        for film in films
    ]


@router.get(
    "/search",
    response_model=list[FilmListOut],
    summary="Films search results",
    response_description="Films search results.",
)
@cache(expire=60 * settings.CACHE_EXPIRATION)
async def films_search(
    query: str | None = None,
    paginator: Paginator = Depends(get_paginator_params),
    service: FilmService = Depends(get_film_service),
    genre_service: GenreServie = Depends(get_genre_service),
    sort_field: Optional[str] = None,
    genre_uuid: Optional[str] = None,
) -> list[FilmListOut]:
    # Получим имя жанра по его uuid
    genre_name = None
    if genre_uuid:
        genre_name = await genre_service.get_by_id(genre_uuid)
        # Доп. проверка на 'NoneType' object has no attribute 'name'
        genre_name = genre_name.name if genre_name else genre_name

    films, page_qty = await service.search_objects(
        query=query,
        size=paginator.page_size,
        page_number=paginator.page_number,
        sort=sort_field,
        genre_name=genre_name,
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return [FilmListOut(id=film.id, title=film.title, imdb_rating=film.imdb_rating) for film in films]


@router.get(
    "/{film_uuid}",
    response_model=Film,
    summary="Film data",
    response_description="Get info about the film.",
)
@cache(expire=60 * settings.CACHE_EXPIRATION)
async def film(
    film_uuid: UUID,
    service: FilmService = Depends(get_film_service),
) -> Film:
    data = await service.get_by_id(film_uuid)

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return data
