"""Database connection: one engine for the app, one session per request."""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# pool_pre_ping checks a connection is alive before using it, so a restarted
# Postgres container doesn't cause errors on the next request.
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Parent class for table models you add later."""


def get_db() -> Iterator[Session]:
    """FastAPI dependency: opens a session for one request, then closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
