import aiohttp
from config import AUTH_GET_PUBLIC_KEY_URL, REDIS_HOST, REDIS_PASSWORD
from managers.RedisManager import RedisManager


class AuthManager:


    async def public_key_init(self):
        async with aiohttp.ClientSession() as client_session:
            async with client_session.get(AUTH_GET_PUBLIC_KEY_URL) as response:
                if not response.ok:
                    raise Exception(f"Error while getting public key ({response.status})")
                data = await response.json()
                key = data.get("key")
                if not key:
                    raise Exception(f"Error while getting public key (key not found in response)")
                
                redis = RedisManager()
                await redis.r.set("auth_public_key", key)

                return key

    async def get_auth_public_key(self):
        ...

