from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Shared properties #
class PermissionBase(BaseModel):
    """Base Permission schema with shared properties."""
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None

# Properties to receive via API on creation #
class PermissionCreate(PermissionBase):
    """Schema for permission creation requests."""
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=100)

# Properties to receive via API on update #
class PermissionUpdate(PermissionBase):
    """Schema for permission update requests."""
    pass

# Additional properties stored in DB #
class PermissionInDBBase(PermissionBase):
    """Base schema for permissions as stored in DB."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Properties to return via API #
class Permission(PermissionInDBBase):
    """Schema for permission responses."""
    pass