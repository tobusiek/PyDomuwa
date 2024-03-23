from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SESSION_MIDDLEWARE_KEY: str = Field(frozen=True)
    API_PORT: int = Field(default=8080, frozen=True)
    DATABASE_URL: str = Field(frozen=True)
    TESTING: bool = Field(default=False)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore
