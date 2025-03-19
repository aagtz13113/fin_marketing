from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session 

from app.core.config import settings

# Create database engine #
engine = create_engine(
    str(settings.DATABASE_URI),
    pool_pre_ping=True,  # Verify connection before using it #
    echo=settings.ENVIRONMENT == "development"  # Log SQL in development mode #
)

# Create session factory #
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI dependency to get a DB session #
def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get a SQLAlchemy database session. 

    This function will be used as a FastAPI dependency to provide
    database sessions to API endpoint functions. It ensures the session
    is properly closed after use.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()