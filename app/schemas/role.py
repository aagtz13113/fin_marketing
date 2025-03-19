from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Shared properties #
class RoleBase(BaseModel):
    """Base Role schema with shared properties."""
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = False
    organization_id: Optional[str] = None

# Properties to receive via API on creation #
class RoleCreate(RoleBase):
    """Schema for role creation requests."""
    name: str = Field(..., min_length=1, max_length=100)

# Properties to receive API on update #
class RoleUpdate(RoleBase):
    """Schema for role update requests."""
    pass

# Additional properties stored in DB #
class RoleInDBBase(RoleBase):
    """Base schema for roles as stored in DB."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return via API #
class Role(RoleInDBBase):
    """Schema for role responses."""
    pass

# Schema for role with permissions #
class RoleWithPermissions(Role):
    """Schema for role with associated permissions."""
    permissions: List["PermissionBase"] = []

# Schema for assigning or removing permissions from a role # 
class UserRoles(BaseModel):
    """Schema for user-role operations."""
    role_ids: List[int]

# Avoid circular import issues with permissions #
from app.schemas.permission import PermissionBase
RoleWithPermissions.model_rebuild()