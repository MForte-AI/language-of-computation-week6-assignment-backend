"""FastAPI application entry point."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.database import get_db

app = FastAPI(title="Week 6 Assignment Backend")


@app.get("/")
def read_root():
    return {"message": "Week 6 backend is running"}


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """Report whether the app can reach PostgreSQL."""
    try:
        db.execute(text("SELECT 1"))
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database unavailable")
    return {"status": "ok", "database": "connected"}
