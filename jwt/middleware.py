#jwt/middleware.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from jwt.tokens import decode_token
from jwt.exceptions import InvalidToken


class JWTAuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(("/auth", "/docs", "/openapi")):
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth:
            return await call_next(request)

        scheme, _, token = auth.partition(" ")
        if scheme.lower() != "bearer":
            raise InvalidToken

        payload = decode_token(token)
        request.state.user_id = int(payload["sub"])

        return await call_next(request)
