#apps/metrics/routers.py

from fastapi import APIRouter
from infra_redis.stats import r

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/")
async def metrics():
    keys = await r.keys("stats:*")

    data = {}
    for k in keys:
        data[k] = int(await r.get(k) or 0)

    return data