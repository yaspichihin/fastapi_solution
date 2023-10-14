from functools import lru_cache
from fastapi import Depends
from pydantic import BaseModel

from src.services.base_service import BaseService
from src.db.elastic_extractor import ElasticExtractor, get_elastic_extractor


allowed_sort_fields = ("imdb_rating",)
directions = {"-": "desc", "+": "asc"}


class FilmService(BaseService):
    def __init__(self, es_extractor: ElasticExtractor):
        super().__init__("movies", es_extractor)

    async def get_all(self, *args, **kwargs) -> tuple[list[BaseModel] | None, int]:
        # Логика сортировки запроса в elastic
        # Дополнительно проводим валидацию поля и знака сортировки
        sort = kwargs.get("sort")
        sorted_field = None
        if sort and len(sort) > 1:
            sign, field = sort[0], sort[1:]
            if field in allowed_sort_fields and sign in directions:
                sorted_field = f"{field}:{directions.get(sign)}"

        # Логика фильтрации по genre
        query_dict = None
        if kwargs.get("genre_name"):
            query_dict = {"bool": {"filter": {"term": {"genre": kwargs.get("genre_name")}}}}

        return await super().get_all(
            size=kwargs.get("size"),
            page_number=kwargs.get("page_number"),
            sort=sorted_field,
            query=query_dict,
        )

    async def search_objects(self, *args, **kwargs) -> tuple[list[BaseModel] | None, int]:
        # Логика сортировки запроса в elastic
        # Дополнительно проводим валидацию поля и знака сортировки
        sort = kwargs.get("sort")
        sorted_field = None
        if sort and len(sort) > 1:
            sign, field = sort[0], sort[1:]
            if field in allowed_sort_fields and sign in directions:
                sorted_field = f"{field}:{directions.get(sign)}"

        # Логика фильтрации по genre
        query = {
            "bool": {
                "should": [
                    {"term": {"genre": kwargs.get("query")}},
                    {"match": {"title": kwargs.get("query")}},
                    {"match": {"description": kwargs.get("query")}},
                    {"term": {"director": kwargs.get("query")}},
                    {"term": {"actors_names": kwargs.get("query")}},
                    {"term": {"writers_names": kwargs.get("query")}},
                ],
            }
        }

        if kwargs.get("genre_name"):
            filter_query: dict = {"filter": {"term": {"genre": kwargs.get("genre_name")}}}

            query["bool"].update(filter_query)

        return await super().search_objects(
            size=kwargs.get("size"),
            page_number=kwargs.get("page_number"),
            sort=sorted_field,
            query=query,
        )


@lru_cache()
def get_film_service(
    es_extractor: ElasticExtractor = Depends(get_elastic_extractor),
) -> FilmService:
    return FilmService(es_extractor)
