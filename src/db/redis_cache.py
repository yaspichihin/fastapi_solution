from typing import Optional
from redis.asyncio import Redis


class RedisCache:
    def __init__(self, host: str, port: int):
        self.redis = Redis(host=host, port=port)

    async def close(self):
        await self.redis.close()


redis_cache: Optional[RedisCache] = None


async def get_redis_cache() -> Redis:
    return redis_cache.redis
