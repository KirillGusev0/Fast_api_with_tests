# settings_pack/settings.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---------- DATABASE ----------
    DB_HOST: str = Field(default="localhost", min_length=1)
    DB_PORT: int = Field(default=5432, ge=1, le=65535)
    DB_USER: str = Field(default="postgres", min_length=1)
    DB_PASS: str = Field(default="qwe", min_length=1)
    DB_NAME: str = Field(default="fastapi_db", min_length=1)

    DATABASE_URL: str | None = None

    # ---------- JWT ----------
    JWT_SECRET: str = Field(default="", min_length=32)
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15, ge=1)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, ge=1)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


    TESTING: bool = False
    
    
    @property
    def db_url(self) -> str:
        if self.TESTING:
            return (
                f"postgresql+asyncpg://"
                f"{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/fastapi_db_test"
            )

        if self.DATABASE_URL:
            return self.DATABASE_URL

        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


    


settings = Settings()



