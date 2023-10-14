from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.v1 import genres, persons, films
from src.core.config import settings
from src.db import elastic_extractor, redis_cache

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    elastic_extractor.es_extractor = elastic_extractor.ElasticExtractor(
        "http://{host}:{port}".format(host=settings.ELASTIC_HOST, port=settings.ELASTIC_PORT)
    )
    redis_cache.redis_cache = redis_cache.RedisCache(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    FastAPICache.init(RedisBackend(await redis_cache.get_redis_cache()), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown():
    await elastic_extractor.es_extractor.close()
    await redis_cache.redis_cache.close()


app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
