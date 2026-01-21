#apps/project/routers.py
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.project.controllers import ProjectController
from apps.project.schemas import (
    ProjectCreateSchema,
    ProjectUpdateSchema,
    ProjectReadSchema,
    ProjectListResponseSchema,
)
from apps.project.services import ProjectService
from apps.project.repository import ProjectRepository
from db.database import async_session


router = APIRouter(prefix="/projects", tags=["Projects"])


async def get_session():
    async with async_session() as session:
        yield session



async def get_project_controller() -> ProjectController:
    repository = ProjectRepository()
    service = ProjectService(repository)
    return ProjectController(service)

@router.get("/{project_id}", response_model=ProjectReadSchema)
async def get_project( project_id: int, session: AsyncSession = Depends(get_session), controller: ProjectController = Depends(get_project_controller)):
    return await controller.get_one(session, project_id)


@router.get("", response_model=ProjectListResponseSchema)
async def get_projects( page: int = Query(1, ge=1), limit: int = Query(10, le=100), status: str | None = None, person_in_charge_id: int | None = None, 
    order_by: str | None = None, session: AsyncSession = Depends(get_session), controller: ProjectController = Depends(get_project_controller)):
    return await controller.get_list(
        session=session,
        page=page,
        limit=limit,
        status=status,
        person_in_charge_id=person_in_charge_id,
        order_by=order_by,
    )


@router.post("", response_model=ProjectReadSchema, status_code=status.HTTP_201_CREATED)
async def create_project( data: ProjectCreateSchema, session: AsyncSession = Depends(get_session), controller: ProjectController = Depends(get_project_controller)):
    return await controller.create(session, data)


@router.put("/{project_id}", response_model=ProjectReadSchema)
async def update_project(project_id: int, data: ProjectUpdateSchema, session: AsyncSession = Depends(get_session), controller: ProjectController = Depends(get_project_controller)):
    return await controller.update(session, project_id, data)


@router.delete("/{project_id}", response_model=ProjectReadSchema)
async def delete_project(project_id: int, session: AsyncSession = Depends(get_session), controller: ProjectController = Depends(get_project_controller)):
    return await controller.delete(session, project_id)
