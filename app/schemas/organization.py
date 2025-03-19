from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, EmailStr

# Shared properties #
class OrganizationBase(BaseModel):
    """Base Organization schema with shared properties."""
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    is_active: Optional[bool] = True
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None

# Properties to receive via API on creation #
class OrganizationCreate(OrganizationBase):
    """Schema for organization creation requests."""
    name: str = Field(..., min_length=1, max_length=255)

# Properties to receive via API on update #
class OrganizationUpdate(OrganizationBase):
    """Schema for organization update requests."""
    pass

# Additional properties stored in DB #
class OrganizationInDBBase(OrganizationBase):
    """Base schema for organizations as stored in DB."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return via API #
class Organization(OrganizationInDBBase):
    """Schema for organization responses."""
    pass