import asyncio

import backoff
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import config


@backoff.on_exception(backoff.expo, Exception)
async def ping_redis():
    r = await Redis.from_url(f"redis://{config.redis_host}:{config.redis_port}")
    await r.ping()
    await r.close()


@backoff.on_exception(backoff.expo, Exception)
async def ping_es():
    print("before es client")
    print(config.es_host)
    client = AsyncElasticsearch(hosts=config.es_host)
    print("after es client")
    if not await client.ping():
        await client.close()
        raise Exception
    await client.close()


async def wait():
    await ping_redis()
    await ping_es()


if __name__ == "__main__":
    asyncio.run(wait())
