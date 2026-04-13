# apps/user/routers.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from apps.user.controllers import UserController
from apps.user.repository import UserRepository
from apps.user.services import UserService
from apps.user.schemas import UserCreateSchema, UserReadSchema, UserUpdateSchema


router = APIRouter(prefix="/users", tags=["users"])


def get_user_controller() -> UserController:
    repository = UserRepository()
    service = UserService(repository)
    return UserController(service)


@router.post("/", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def create_user( data: UserCreateSchema, controller: UserController = Depends(get_user_controller)):
    return await controller.create_user(data)


@router.post("/bulk", response_model=List[UserReadSchema], status_code=status.HTTP_201_CREATED,)
async def create_users_bulk(data: List[UserCreateSchema], controller: UserController = Depends(get_user_controller)):
    return await controller.create_users_bulk(data)


@router.get("/", response_model=List[UserReadSchema])
async def get_users(controller: UserController = Depends(get_user_controller)):
    return await controller.get_users()


@router.get("/ids", response_model=List[UserReadSchema])
async def get_users_by_ids(ids: str, controller: UserController = Depends(get_user_controller)):
    try:
        user_ids = [int(i) for i in ids.split(",") if i.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ids format")

    return await controller.get_users_by_ids(user_ids)


@router.get("/{user_id}", response_model=UserReadSchema)
async def get_user(user_id: int, controller: UserController = Depends(get_user_controller)):
    user = await controller.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserReadSchema)
async def update_user(user_id: int, data: UserUpdateSchema, controller: UserController = Depends(get_user_controller)):
    user = await controller.update_user(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=UserReadSchema)
async def delete_user(user_id: int, controller: UserController = Depends(get_user_controller)):
    user = await controller.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
