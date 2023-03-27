from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from config.config import get_env

X_API_KEY = get_env("auth", "x-api-key", "x-api-key not configured")

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="API x-api-key not found in header"
        )

    if api_key_header != X_API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="API x-api-key is invalid"
        )

    return api_key_header