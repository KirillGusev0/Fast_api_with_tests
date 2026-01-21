#app/auth/controllers.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.auth.services import AuthService
from apps.auth.repository import UserAuthRepository

                        

def get_auth_service() -> AuthService:
    return AuthService(UserAuthRepository())


class AuthController:

    def __init__(self, service: AuthService = Depends(get_auth_service)):
        self.service = service

    async def login(self, data, session: AsyncSession):
        return await self.service.login(session, data.username, data.password)

    async def refresh(self, data):
        return await self.service.refresh(data.refresh_token)

    async def get_current_user(self, session: AsyncSession, token: str):
        return await self.service.get_current_user(session, token)
