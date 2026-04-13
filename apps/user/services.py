# apps/user/services.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from security.password import hash_password
from apps.user.repository import UserRepository
from apps.user.schemas import UserCreateSchema, UserUpdateSchema
from apps.user.models import Users


from infra_redis.cache_utils import cached, invalidate, invalidate_many

class UserService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    @invalidate(lambda self, session, data: "users:all")
    async def create_user(self, session: AsyncSession, data: UserCreateSchema) -> Users:
        user = Users(
            name=data.name,
            username=data.username,
            hashed_password=hash_password(data.password),
            email=data.email,
        )
        return await self.repo.create(session, user)

    @invalidate(lambda self, session, data_list: "users:all")
    async def create_many(self, session: AsyncSession, data_list: List[UserCreateSchema]) -> List[Users]:
        users = [
            Users(
                name=d.name,
                username=d.username,
                hashed_password=hash_password(d.password),
                email=d.email,
            )
            for d in data_list
        ]
        return await self.repo.create_many(session, users)

    @cached(lambda self, session: "users:all", ttl=60)
    async def get_all(self, session: AsyncSession) -> List[Users]:
        return await self.repo.get_all(session)

    @cached(lambda self, session, user_id: f"user:{user_id}", ttl=300)
    async def get_by_id(self, session: AsyncSession, user_id: int) -> Optional[Users]:
        return await self.repo.get_by_id(session, user_id)

    @invalidate_many( lambda self, session, user_id, payload: f"user:{user_id}", lambda self, session, user_id, payload: "users:all")
    async def update_user(self, session: AsyncSession, user_id: int, payload: UserUpdateSchema) -> Optional[Users]:
        data = payload.dict(exclude_unset=True)

        if "password" in data:
            data["hashed_password"] = hash_password(data.pop("password"))

        return await self.repo.update(session, user_id, data)


    @invalidate_many( lambda self, session, user_id: f"user:{user_id}", lambda self, session, user_id: "users:all")
    async def delete_user(self, session: AsyncSession, user_id: int) -> Optional[Users]:
        return await self.repo.delete(session, user_id)
    
    @cached(lambda self, session, username: f"user:username:{username}", ttl=300)
    async def get_by_username( self, session: AsyncSession, username: str) -> Optional[Users]:
        return await self.repo.get_by_username(session, username)
    
    
