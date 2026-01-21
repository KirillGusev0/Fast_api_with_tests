#jwt/config.py
from datetime import timedelta
from settings_pack.settings import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

REFRESH_TOKEN_EXPIRE = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)