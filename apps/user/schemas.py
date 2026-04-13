#apps/user/schemas.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBaseSchema(BaseModel):
    name: str = Field(min_length=1)
    username: str = Field(min_length=1)
    email: Optional[EmailStr] = None


class UserCreateSchema(UserBaseSchema):
    password: str = Field(min_length=1)


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserReadSchema(UserBaseSchema):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

