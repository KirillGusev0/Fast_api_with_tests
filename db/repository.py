#db/repository.py
from db.database import async_session

class BaseRepository:
    async_session = async_session