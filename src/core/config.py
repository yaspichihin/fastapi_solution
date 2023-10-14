import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PROJECT_NAME: str = Field("movies", alias="PROJECT_NAME")

    REDIS_HOST: str = Field("127.0.0.1", alias="REDIS_HOST")
    REDIS_PORT: int = Field(6379, alias="REDIS_PORT")

    ELASTIC_HOST: str = Field("127.0.0.1", alias="ELASTIC_HOST")
    ELASTIC_PORT: int = Field(9200, alias="ELASTIC_PORT")

    LOGGING_LEVEL: str = Field("DEBUG", alias="LOGGING_LEVEL")

    BASE_DIR: str = Field(os.path.dirname(os.path.abspath(__file__)))

    PAGE_SIZE: int = Field(50, alias="PAGE_SIZE")
    SCROLL_TIME: str = Field("2m", alias="SCROLL_TIME")

    CACHE_EXPIRATION: int = Field(5, alias="CACHE_EXPIRATION")


settings = Config()
