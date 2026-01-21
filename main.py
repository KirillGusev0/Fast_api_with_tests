#main.py
from fastapi import FastAPI
from jwt.middleware import JWTAuthMiddleware
from db import models  # noqa: F401
from routers.api_v1_routers import api_router


app = FastAPI()

app.add_middleware(JWTAuthMiddleware)

app.include_router(api_router)
