#tests/controllers/test_project_controller.py

import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timezone

from main import app
from apps.project.routers import get_project_controller


class FakeProjectController:
    async def create(self, session, data):
        return {
            "project_id": 1,
            "title": data.title,
            "description": data.description,
            "status": data.status,
            "create_time": datetime.now(timezone.utc),
        }

    async def get_one(self, session, project_id):
        return {
            "project_id": project_id,
            "title": "Project",
            "status": "new",
            "create_time": datetime.now(timezone.utc),
        }

    async def get_list(self, session, page, limit, **_):
        return {
            "items": [
                {
                    "project_id": 1,
                    "title": "P1",
                    "status": "new",
                    "create_time": datetime.now(timezone.utc),
                },
                {
                    "project_id": 2,
                    "title": "P2",
                    "status": "new",
                    "create_time": datetime.now(timezone.utc),
                },
            ],
            "total_count": 2,
            "has_prev": False,
            "has_next": False,
        }


@pytest.mark.controllers
@pytest.mark.asyncio
async def test_create_project():
    app.dependency_overrides[get_project_controller] = lambda: FakeProjectController()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/api/v1/project/projects",
            json={
                "title": "Test Project",
                "description": "Desc",
                "status": "new",
            },
        )

    assert response.status_code == 201
    assert response.json()["project_id"] == 1

    app.dependency_overrides.clear()


@pytest.mark.controllers
@pytest.mark.asyncio
async def test_get_project_by_id():
    app.dependency_overrides[get_project_controller] = lambda: FakeProjectController()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/api/v1/project/projects/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Project"

    app.dependency_overrides.clear()


@pytest.mark.controllers
@pytest.mark.asyncio
async def test_get_projects_list():
    app.dependency_overrides[get_project_controller] = lambda: FakeProjectController()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/api/v1/project/projects")

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total_count"] == 2

    app.dependency_overrides.clear()
