#apps/external/routers.py

from fastapi import APIRouter, Depends

from apps.external.services.posts_service import ExternalPostsService

router = APIRouter(tags=["External"])

def get_external_posts_service():
    return ExternalPostsService()

@router.get("/posts")
async def get_external_posts( service: ExternalPostsService = Depends(get_external_posts_service)):
    return await service.fetch_posts()
