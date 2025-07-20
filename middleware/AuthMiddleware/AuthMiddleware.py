from starlette.middleware.base import BaseHTTPMiddleware
import time
from fastapi import Request, HTTPException, status
from managers.AuthManager import JWTManager, AuthManager
from managers.Logger import AsyncLogger


logger = AsyncLogger()


ex401 = HTTPException(401, "Unauthorized")
ex403 = HTTPException(403, "Forbidden")
jwt_m: JWTManager = JWTManager()


def get_bearer_token(request: Request) -> str:
    auth: str = request.headers.get("Authorization")

    if not auth or not auth.lower().startswith("bearer "):
        return None

    token = auth[7:]
    return token


async def admin_required(request: Request):
    token = get_bearer_token(request)
    if not token:
        raise ex401
    auth_manager = AuthManager()
    data = jwt_m.get_data(token, await auth_manager.get_auth_public_key())
    await logger.info(f"JWT decoded data: '{data}', token:{token}")
    if (not data) or (not data.get("is_admin")):
        raise ex403

    return data


async def user_required(request: Request):
    token = get_bearer_token(request)
    if not token:
        raise ex401
    auth_manager = AuthManager()
    data = jwt_m.get_data(token, await auth_manager.get_auth_public_key())
    await logger.info(f"JWT decoded data: '{data}', token:{token}")
    if not data:
        raise ex401

    return data
