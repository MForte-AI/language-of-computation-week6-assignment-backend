"""App settings, read from environment variables or the .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://week6:week6_dev_password@localhost:5432/week6"


settings = Settings()
