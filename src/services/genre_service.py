from functools import lru_cache

from fastapi import Depends

from src.services.base_service import BaseService
from src.db.elastic_extractor import ElasticExtractor, get_elastic_extractor


class GenreServie(BaseService):
    def __init__(self, es_extractor: ElasticExtractor):
        super().__init__("genres", es_extractor)


@lru_cache()
def get_genre_service(es_extractor: ElasticExtractor = Depends(get_elastic_extractor)) -> GenreServie:
    return GenreServie(es_extractor)
