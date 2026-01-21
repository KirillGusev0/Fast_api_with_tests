# tests/services/test_user_service.py

import pytest
from unittest.mock import AsyncMock, MagicMock

from apps.user.services import UserService
from apps.user.models import Users
from apps.user.schemas import UserCreateSchema


@pytest.mark.services
@pytest.mark.asyncio
async def test_create_user():
    repo = AsyncMock()

    data = UserCreateSchema(
        name="Test User",
        username="testuser",
        email="test@mail.com",
        password="123456",
    )

    fake_user = Users(
        name=data.name,
        username=data.username,
        email=data.email,
        hashed_password="hashed",
    )

    repo.create.return_value = fake_user

    service = UserService(repository=repo)
    result = await service.create_user(repo, data)

    repo.create.assert_called_once()
    assert result == fake_user



@pytest.mark.services
@pytest.mark.asyncio
async def test_get_user_by_id_found():
    repo = AsyncMock()

    fake_user = Users(
        user_id=1,
        name="User",
        username="user1",
        hashed_password="hashed",
    )

    repo.get_by_id.return_value = fake_user

    service = UserService(repository=repo)
    result = await service.get_by_id(repo, 1)

    repo.get_by_id.assert_called_once_with(repo, 1)
    assert result == fake_user



@pytest.mark.services
@pytest.mark.asyncio
async def test_get_user_by_id_not_found():
    repo = AsyncMock()
    repo.get_by_id.return_value = None 

    service = UserService(repository=repo)
    result = await service.get_by_id(repo, 999)

    assert result is None



@pytest.mark.services
@pytest.mark.asyncio
async def test_get_user_by_username():
    repo = AsyncMock()

    fake_user = Users(
        user_id=1,
        name="User",
        username="user1",
        hashed_password="hashed",
    )

    repo.get_by_username.return_value = fake_user

    service = UserService(repository=repo)
    result = await service.get_by_username(repo, "user1")

    repo.get_by_username.assert_called_once_with(repo, "user1")
    assert result == fake_user

