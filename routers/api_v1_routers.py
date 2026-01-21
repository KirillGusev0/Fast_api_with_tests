#routers/api_v1_routers.py
from fastapi import APIRouter

from apps.user.routers import router as user_router
from apps.auth.routers import router as auth_router
from apps.project.routers import router as project_router
from apps.external.routers import router as external_router



api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(user_router, prefix="/users")
api_router.include_router(project_router, prefix="/project")
api_router.include_router(external_router, prefix="/external")