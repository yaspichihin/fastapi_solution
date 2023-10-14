from functools import lru_cache

from fastapi import Depends

from src.services.base_service import BaseService
from src.db.elastic_extractor import ElasticExtractor, get_elastic_extractor


class PersonService(BaseService):
    def __init__(self, es_extractor: ElasticExtractor):
        super().__init__("persons", es_extractor)


@lru_cache()
def get_person_service(es_extractor: ElasticExtractor = Depends(get_elastic_extractor)) -> PersonService:
    return PersonService(es_extractor)
