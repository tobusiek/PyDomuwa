from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SESSION_MIDDLEWARE_KEY: str = Field(default="gucci", frozen=True)
    API_PORT: int = Field(default=8080, frozen=True)
    DATABASE_URL: str = Field(default="sqlite:///db.sqlite3", frozen=True)
    ALLOWED_ORIGINS: list[str] = Field(default=["*"], frozen=True)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
