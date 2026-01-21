#apps/project/servises.py
from sqlalchemy.ext.asyncio import AsyncSession

from apps.project.models import Project
from apps.project.repository import ProjectRepository
from apps.project.schemas import ProjectCreateSchema, ProjectUpdateSchema


class ProjectService:

    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def get_project(self, session: AsyncSession, project_id: int) -> Project:
        project = await self.repository.get_by_id(session, project_id)
        if not project:
            raise ValueError("Project not found")
        return project

    async def get_projects(self, session: AsyncSession, page: int, limit: int, **filters,):
        offset = (page - 1) * limit
        items, total = await self.repository.get_list(
            session=session,
            offset=offset,
            limit=limit,
            **filters,
        )

        return {
            "items": items,
            "total_count": total,
            "has_prev": page > 1,
            "has_next": offset + limit < total,
        }

    async def create_project(self, session: AsyncSession, data: ProjectCreateSchema,) -> Project:
        project = Project(**data.model_dump())
        return await self.repository.create(session, project)

    async def update_project(self, session: AsyncSession, project_id: int, data: ProjectUpdateSchema,) -> Project:
        project = await self.get_project(session, project_id)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)

        return project

    async def delete_project(self, session: AsyncSession, project_id: int,) -> Project:
        return await self.repository.delete(session, project_id)
