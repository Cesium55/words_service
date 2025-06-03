import aiohttp
from redis.asyncio import Redis
from config import REDIS_HOST, REDIS_PASSWORD



class RedisManager:
    r: Redis

    def __init__(self, redis_host=REDIS_HOST, redis_password=REDIS_PASSWORD):
        self.r = Redis(host=redis_host, decode_responses=True)
