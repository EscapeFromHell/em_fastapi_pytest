from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api_v1"
    REDIS_URL: str = "redis://redis:6379"
    REDIS_EXPIRATION_TIME: int = 24 * 60 * 60
    URL: str = "https://spimex.com/upload/reports/oil_xls/oil_xls_"
    USER: str = "postgres"
    PASSWORD: str = "password"
    HOST: str = "spimex-fastapi-db"
    PORT: str = "5432"
    NAME: str = "spimex-fastapi"
    USER_TEST: str = "postgres-test"
    PASSWORD_TEST: str = "password-test"
    HOST_TEST: str = "spimex-fastapi-db-test"
    PORT_TEST: str = "5433"
    NAME_TEST: str = "spimex-fastapi-test"

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    @property
    def TEST_DB_URL(self):
        return f"postgresql+asyncpg://{self.USER_TEST}:{self.PASSWORD_TEST}@{self.HOST_TEST}:{self.PORT_TEST}/{self.NAME_TEST}"

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost",
        "http://127.0.0.1",
    ]
    BACKEND_HOST_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost",
        "http://127.0.0.1",
    ]

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
