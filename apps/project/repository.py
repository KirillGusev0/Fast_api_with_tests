#apps/project/repository.py

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from apps.project.models import Project, ProjectStatus
from db.repository import BaseRepository


class ProjectRepository(BaseRepository):

    async def get_by_id(self, session: AsyncSession, project_id: int) -> Project | None:
        """
        SELECT * FROM projects WHERE project_id = :project_id;
        """
        result = await session.execute(
            select(Project).where(Project.project_id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        session: AsyncSession,
        offset: int,
        limit: int,
        status: ProjectStatus | None = None,
        person_in_charge_id: int | None = None,
        order_by: str | None = None,
    ):
        """
        SELECT * FROM projects
        WHERE (:status IS NULL OR status = :status)
        AND (:user_id IS NULL OR person_in_charge_id = :user_id)
        ORDER BY create_time DESC
        LIMIT :limit OFFSET :offset;
        """
        query = select(Project)

        if status:
            query = query.where(Project.status == status)

        if person_in_charge_id:
            query = query.where(Project.person_in_charge_id == person_in_charge_id)

        if order_by == "create_time":
            query = query.order_by(Project.create_time.desc())
        elif order_by == "start_time":
            query = query.order_by(Project.start_time.desc())
        elif order_by == "complete_time":
            query = query.order_by(Project.complete_time.desc())

        total = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        result = await session.execute(
            query.offset(offset).limit(limit)
        )

        return result.scalars().all(), total

    async def create(self, session: AsyncSession, project: Project) -> Project:
        """
        INSERT INTO projects (...) VALUES (...);
        """
        session.add(project)
        await session.flush()
        return project

    async def delete(self, session: AsyncSession, project_id: int) -> Project:
        """
        DELETE FROM projects WHERE project_id = :project_id RETURNING *;
        """
        project = await self.get_by_id(session, project_id)
        await session.delete(project)
        return project
