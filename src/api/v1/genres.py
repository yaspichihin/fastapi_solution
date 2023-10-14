from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.api.v1.output_schemas.schema_genres import GenreOut, GenresListOut
from src.models.paginator import Paginator, get_paginator_params
from src.services.genre_service import GenreServie, get_genre_service
from src.core.config import settings

router = APIRouter()


@router.get(
    "/{genre_id}",
    response_model=GenreOut,
    summary="Genre data",
    response_description="Get info about the genre with id, name",
)
@cache(expire=60 * settings.CACHE_EXPIRATION)
async def genre_details(genre_id: str, genre_service: GenreServie = Depends(get_genre_service)) -> GenreOut:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")
    return GenreOut(id=genre.id, name=genre.name)


@router.get(
    "/",
    response_model=List[GenresListOut],
    summary="Genres list",
    response_description="Get a list of all genres.",
)
@cache(expire=60 * settings.CACHE_EXPIRATION)
async def genres_list(
    paginator: Paginator = Depends(get_paginator_params), genre_service: GenreServie = Depends(get_genre_service)
) -> List[GenresListOut]:
    genres, page_ty = await genre_service.get_all(
        size=paginator.page_size,
        page_number=paginator.page_number,
    )
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")
    return [GenresListOut(id=genre.id, name=genre.name) for genre in genres]
