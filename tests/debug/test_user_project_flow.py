#tests/debug/test_user_project_flow.py
import pytest

from apps.user.services import UserService
from apps.project.services import ProjectService
from apps.user.schemas import UserCreateSchema
from apps.project.schemas import ProjectCreateSchema
from apps.user.repository import UserRepository
from apps.project.repository import ProjectRepository

@pytest.mark.debug
@pytest.mark.asyncio
async def test_user_can_be_person_in_charge(db_session):

    user_service = UserService(UserRepository())
    project_service = ProjectService(ProjectRepository())

    user = await user_service.create_user(
        db_session,
        UserCreateSchema(
            name="Debug User",
            username="debug_user",
            email="debug@test.com",
            password="password123",
        ),
    )

    project = await project_service.create_project(
        db_session,
        ProjectCreateSchema(
            title="Debug Project",
            description="Debug flow",
            person_in_charge_id=user.user_id,
        ),
    )

    assert project.person_in_charge_id == user.user_id

