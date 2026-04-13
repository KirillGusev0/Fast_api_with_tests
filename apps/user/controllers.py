# apps/user/controllers.py
from typing import List, Optional

from apps.user.services import UserService
from apps.user.schemas import UserCreateSchema, UserUpdateSchema
from apps.user.models import Users


class UserController:
    def __init__(self, service: UserService):
        self.service = service

    async def get_user(self, user_id: int) -> Optional[Users]:
        return await self.service.get_by_id(user_id)

    async def get_users(self) -> List[Users]:
        return await self.service.get_all()

    async def get_users_by_ids(self, user_ids: List[int]) -> List[Users]:
        return await self.service.get_by_ids(user_ids)

    async def create_user(self, data: UserCreateSchema) -> Users:
        return await self.service.create_user(data)

    async def create_users_bulk(self, data: List[UserCreateSchema]) -> List[Users]:
        return await self.service.create_many(data)

    async def update_user(self, user_id: int, data: UserUpdateSchema) -> Optional[Users]:
        return await self.service.update_user(user_id, data)

    async def delete_user(self, user_id: int) -> Optional[Users]:
        return await self.service.delete_user(user_id)
