#jwt/dependencies.py

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from jwt.tokens import decode_token
from jwt.exceptions import InvalidToken
from db.session import get_async_session
from apps.user.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise InvalidToken

    user_id = int(payload["sub"])
    user = await UserRepository.get_by_user_id(session, user_id)

    if not user:
        raise InvalidToken

    return user
