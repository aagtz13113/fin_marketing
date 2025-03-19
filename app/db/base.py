from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, func

# Create declarative base class #
Base = declarative_base()

# Base model class for common fields and methods #
class BaseModel:
    """
    Base model class that can be used for all models to include common fields.

    Provides:
    - ID primary key
    - created_at timestamp
    - updated_at timestamp that auto-updates on changes
    """
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

# Import all models here for Alembic to discover them #
# This avoids circular imports when models reference each other #
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission 