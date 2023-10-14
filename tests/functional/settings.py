from pydantic import Field
from pydantic_settings import BaseSettings

from tests.functional.testdata.es_mappings import index_mappings, index_settings


class Config(BaseSettings):
    es_host: str = Field("http://127.0.0.1:9200", alias="ELASTIC_URL")
    es_index: str = Field("movies", alias="ES_INDEX")
    es_id_field: str = Field("id", alias="ES_ID_FIELD")
    es_index_settings: dict = Field(index_settings)
    es_index_mapping: dict = Field(index_mappings)

    redis_host: str = Field("127.0.0.1", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")
    service_url: str = Field("http://127.0.0.1:8000", alias="SERVICE_URL")
    page_size: int = Field(15, alias="PAGE_SIZE")


config = Config()
