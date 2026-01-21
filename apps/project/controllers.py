#apps/project/controllers.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.project.repository import ProjectRepository
from apps.project.services import ProjectService



def get_project_service() -> ProjectService:
    return ProjectService(ProjectRepository())


class ProjectController:

    def __init__(self, service: ProjectService = Depends(get_project_service)):
        self.service = service

    async def get_one(self, session: AsyncSession, project_id: int):
        return await self.service.get_project(session, project_id)

    async def get_list(self, session: AsyncSession, **params):
        return await self.service.get_projects(session, **params)

    async def create(self, session: AsyncSession, data):
        return await self.service.create_project(session, data)

    async def update(self, session: AsyncSession, project_id: int, data):
        return await self.service.update_project(session, project_id, data)

    async def delete(self, session: AsyncSession, project_id: int):
        return await self.service.delete_project(session, project_id)
