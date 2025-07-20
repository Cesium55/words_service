import aiohttp
from config import AUTH_GET_PUBLIC_KEY_URL, REDIS_HOST, REDIS_PASSWORD
from managers.RedisManager import RedisManager


class AuthManager:

    public_key_redis_key = "auth_public_key"

    async def public_key_init(self, silent=False):
        async with aiohttp.ClientSession() as client_session:
            async with client_session.get(AUTH_GET_PUBLIC_KEY_URL) as response:
                if not response.ok:
                    raise Exception(
                        f"Error while getting public key ({response.status})"
                    )
                data = await response.json()
                key = data.get("key")
                if (not key) and (not silent):
                    raise Exception(
                        f"Error while getting public key (key not found in response)"
                    )

                redis = RedisManager()
                await redis.set(self.public_key_redis_key, key)

                return key

    async def get_auth_public_key(self, init_if_null=True):
        redis = RedisManager()

        key = await redis.get(self.public_key_redis_key)
        if key:
            return key
        if not init_if_null:
            return None

        key = await self.public_key_init(silent=True)
        return key
