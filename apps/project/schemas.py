#apps/project/schemas.py

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from apps.project.models import ProjectStatus


class ProjectBase(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.new
    start_time: Optional[datetime] = None
    complete_time: Optional[datetime] = None
    person_in_charge_id: Optional[int] = None


class ProjectCreateSchema(ProjectBase):
    pass


class ProjectUpdateSchema(BaseModel):
    title: Optional[str] = Field(min_length=1)
    description: Optional[str]
    status: Optional[ProjectStatus]
    start_time: Optional[datetime]
    complete_time: Optional[datetime]
    person_in_charge_id: Optional[int]


class ProjectReadSchema(ProjectBase):
    project_id: int
    create_time: datetime

    class Config:
        from_attributes = True


class ProjectListResponseSchema(BaseModel):
    items: List[ProjectReadSchema]
    total_count: int
    has_next: bool
    has_prev: bool
