# db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from settings_pack.settings import settings


async_engine = create_async_engine(
    settings.db_url,
    echo=True,
)

async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, column in enumerate(self.__table__.columns.keys()):
            if column in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{column}={getattr(self, column)}")
        return f"<{self.__class__.__name__} {','.join(cols)}>"
