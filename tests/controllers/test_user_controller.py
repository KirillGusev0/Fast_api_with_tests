# tests/controllers/test_user_controller.py
import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from apps.user.routers import get_user_controller
from datetime import datetime

class FakeUserController:
    async def create_user(self, data):
        return {
            "user_id": 1,
            "name": data.name,
            "username": data.username,
            "email": data.email,
            "created_at": datetime.utcnow(),
        }
    
    async def get_user(self, user_id: int):
        if user_id == 999:
            return None
        return {
            "user_id": user_id,
            "name": "Test",
            "username": "testuser",
            "email": "test@mail.com",
            "created_at": datetime.utcnow(),
        }




@pytest.mark.controllers
@pytest.mark.asyncio
async def test_create_user():
    app.dependency_overrides[get_user_controller] = lambda: FakeUserController()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/users/users/",
            json={
                "name": "Test User",
                "username": "testuser",
                "email": "test@mail.com",
                "password": "12345678",
            },
        )

    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

    app.dependency_overrides.clear()


@pytest.mark.controllers
@pytest.mark.asyncio
async def test_get_user_by_id_found():
    app.dependency_overrides[get_user_controller] = lambda: FakeUserController()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/users/users/1")

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

    app.dependency_overrides.clear()


@pytest.mark.controllers
@pytest.mark.asyncio
async def test_get_user_by_id_not_found():
    app.dependency_overrides[get_user_controller] = lambda: FakeUserController()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/users/users/999")

    assert response.status_code == 404

    app.dependency_overrides.clear()
