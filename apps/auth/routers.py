#apps/auth/routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from apps.auth.controllers import AuthController
from apps.auth.schemas import LoginSchema, TokenSchema, RefreshTokenSchema
from db.database import async_session
from typing import AsyncGenerator

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


@router.post("/login", response_model=TokenSchema)
async def login(
    data: LoginSchema,
    session: AsyncSession = Depends(get_session),
    controller: AuthController = Depends(),
):
    try:
        return await controller.login(data, session)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


@router.post("/refresh", response_model=TokenSchema)
async def refresh(
    data: RefreshTokenSchema,
    controller: AuthController = Depends(),
):
    try:
        return await controller.refresh(data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
