"""App settings, read from environment variables or the .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://week6:week6_dev_password@localhost:5432/week6"

    # Frontend dev servers allowed to call this API from a browser (CORS).
    # Covers Vite (5173) and Create React App / Next.js (3000). Override in
    # .env with a JSON list, e.g. CORS_ORIGINS=["http://localhost:4200"]
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]


settings = Settings()
