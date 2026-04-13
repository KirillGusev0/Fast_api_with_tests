# apps/user/repository.py
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.user.models import Users


class UserRepository:

    async def create(self, session: AsyncSession, user: Users) -> Users:
        session.add(user)
        await session.flush()
        return user

    async def create_many(self, session: AsyncSession, users: List[Users]) -> List[Users]:
        session.add_all(users)
        await session.flush()
        return users

    async def get_all(self, session: AsyncSession) -> List[Users]:
        result = await session.execute(select(Users))
        return result.scalars().all()

    async def get_by_id(self, session: AsyncSession, user_id: int) -> Optional[Users]:
        result = await session.execute(
            select(Users).where(Users.user_id == user_id)
        )
        return result.scalars().first()

    async def get_by_ids(self, session: AsyncSession, user_ids: List[int]) -> List[Users]:
        result = await session.execute(
            select(Users).where(Users.user_id.in_(user_ids))
        )
        return result.scalars().all()

    async def get_by_username(self, session: AsyncSession, username: str) -> Optional[Users]:
        result = await session.execute(
            select(Users).where(Users.username == username)
        )
        return result.scalars().first()

    async def update(self, session: AsyncSession, user_id: int, data: dict) -> Optional[Users]:
        user = await self.get_by_id(session, user_id)
        if not user:
            return None

        for key, value in data.items():
            setattr(user, key, value)

        await session.flush()
        return user

    async def delete(self, session: AsyncSession, user_id: int) -> Optional[Users]:
        user = await self.get_by_id(session, user_id)
        if not user:
            return None

        await session.delete(user)
        return user
