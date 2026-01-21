#jwt/tokens.py
from datetime import datetime, timezone
from typing import Any, Dict

from jose import jwt, JWTError

from jwt.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE,
    REFRESH_TOKEN_EXPIRE,
)
from jwt.exceptions import InvalidToken, TokenExpired


def _create_token(data: Dict[str, Any], expires_delta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: int) -> str:
    return _create_token(
        data={"sub": str(user_id), "type": "access"},
        expires_delta=ACCESS_TOKEN_EXPIRE,
    )


def create_refresh_token(user_id: int) -> str:
    return _create_token(
        data={"sub": str(user_id), "type": "refresh"},
        expires_delta=REFRESH_TOKEN_EXPIRE,
    )


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise InvalidToken
