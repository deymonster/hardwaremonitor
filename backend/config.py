from pydantic import computed_field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

    # App

    DEBUG: bool = False
    WEB_CONCURRENCY: int = 1
    APP_SECRET_KEY: str
    APP_PORT: int = 8000
    ALLOW_ORIGINS: list[str]
    ALLOW_ORIGIN_REGEX: str

    # Redis

    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"

    # MondoDB
    MONGO_HOST: str
    MONGO_PORT: str
    MONGO_NAME: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str


    @computed_field
    @property
    def REDIS_URL(self) -> str:
        return str(
            RedisDsn.build(  # type: ignore
                scheme="redis",
                host=self.REDIS_HOST,
                port=int(self.REDIS_PORT),
            )
        )

    @computed_field
    @property
    def mongo_url(self) -> str:
        return f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}"

    # Postgres

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str
    POSTGRES_POOL_SIZE: int = 80
    POSTGRES_MAX_OVERFLOW: int = 10

    @computed_field
    @property
    def POSTGRES_POOL_SIZE_BY_SERVER(self) -> int:
        return self.POSTGRES_POOL_SIZE // self.WEB_CONCURRENCY

    @computed_field
    @property
    def DB_ASYNC_CONNECTION_STR(self) -> str:
        return str(
            PostgresDsn.build(  # type: ignore
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=int(self.POSTGRES_PORT),
                path=self.POSTGRES_DB,
            )
        )


settings = Settings(**{})


__all__ = [
    "settings",
]
