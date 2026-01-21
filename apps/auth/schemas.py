#apps/auth/schemas.py

from pydantic import BaseModel
from typing import Optional


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: int
    type: str
