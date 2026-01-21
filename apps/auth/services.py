#apps/auth/services.py
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from settings_pack.settings import settings
from apps.auth.repository import UserAuthRepository
from apps.auth.schemas import TokenSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    def __init__(self, repository: UserAuthRepository):
        self.repository = repository

    # ---------- password ----------

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # ---------- jwt core ----------

    def _create_token(self, subject: int, token_type: str, expires_delta: timedelta) -> str:
        payload = {
            "sub": subject,
            "type": token_type,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + expires_delta,
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

    # ---------- auth ----------

    async def login(self, session: AsyncSession, username: str, password: str) -> TokenSchema:
        user = await self.repository.get_user_by_username(session, username)
        if not user:
            raise ValueError("Invalid credentials")

        if not self.verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        access_token = self._create_token(
            subject=user.user_id,
            token_type="access",
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        )

        refresh_token = self._create_token(
            subject=user.user_id,
            token_type="refresh",
            expires_delta=timedelta(days=settings.refresh_token_expire_days),
        )

        return TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh(self, refresh_token: str) -> TokenSchema:
        payload = self.decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        user_id = payload.get("sub")

        access_token = self._create_token(
            subject=user_id,
            token_type="access",
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        )

        new_refresh_token = self._create_token(
            subject=user_id,
            token_type="refresh",
            expires_delta=timedelta(days=settings.refresh_token_expire_days),
        )

        return TokenSchema(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )

    async def get_current_user(self, session: AsyncSession, token: str):
        payload = self.decode_token(token)

        if payload.get("type") != "access":
            raise ValueError("Invalid token type")

        user_id = payload.get("sub")

        user = await self.repository.get_user_by_id(session, user_id)
        if not user:
            raise ValueError("User not found")

        return user

