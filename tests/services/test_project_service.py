#tests/services/test_project_service.py

import pytest
from unittest.mock import AsyncMock, MagicMock

from apps.project.services import ProjectService
from apps.project.models import Project, ProjectStatus
from apps.project.schemas import ProjectCreateSchema


@pytest.mark.services
@pytest.mark.asyncio
async def test_create_project():
    repo = AsyncMock()
    session = AsyncMock()

    data = ProjectCreateSchema(
        title="Test Project",
        description="Desc",
        status=ProjectStatus.new,
    )

    fake_project = Project(
        title=data.title,
        description=data.description,
        status=data.status,
    )

    repo.create.return_value = fake_project

    service = ProjectService(repository=repo)
    result = await service.create_project(session, data)

    repo.create.assert_called_once()
    assert result == fake_project


@pytest.mark.services
@pytest.mark.asyncio
async def test_get_project_by_id_found():
    

    fake_project = Project(
        project_id=1,
        title="Project",
        status=ProjectStatus.new,
    )

    repo = AsyncMock()
    repo.get_by_id.return_value = fake_project

    service = ProjectService(repository=repo)
    result = await service.get_project(repo, 1)

    repo.get_by_id.assert_called_once_with(repo, 1)
    assert result == fake_project



@pytest.mark.services
@pytest.mark.asyncio
async def test_get_project_by_id_not_found():
    repo = AsyncMock()
    repo.get_by_id.return_value = None

    service = ProjectService(repository=repo)

    with pytest.raises(ValueError, match="Project not found"):
        await service.get_project(repo, 999)




@pytest.mark.services
@pytest.mark.asyncio
async def test_get_projects_list():
    repo = AsyncMock()

    fake_projects = [
        Project(project_id=1, title="P1"),
        Project(project_id=2, title="P2"),
    ]

    repo.get_list.return_value = (fake_projects, 2)

    service = ProjectService(repository=repo)
    result = await service.get_projects(
        session=repo,
        page=1,
        limit=10,
        status=None,
        person_in_charge_id=None,
        order_by=None,
    )

    assert result["items"] == fake_projects
    assert result["total_count"] == 2
    assert result["has_prev"] is False
    assert result["has_next"] is False



