from typing import List, Optional 
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.config import settings

# Shared properties #
class UserBase(BaseModel):
    """Base User schema with shared properties."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True
    organization_id: Optional[int] = None

# Properties to receive via API on creation #
class UserCreate(UserBase):
    """Schema for user creation requests."""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=settings.PASSWORD_MIN_LENGTH)

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        """Validate password strength"""
        min_length = settings.PASSWORD_MIN_LENGTH
        if len(v) < min_length:
            raise ValueError(f'Password must be at least {min_length} characters')
        # Add more validation if needed (uppercase, lowercase, digits, etc.)
        return v
    
# Properties to receive via API on update #
class UserUpdate(UserBase):
    """Schema for user update requests."""
    password: Optional[str] = Field(None, min_length=settings.PASSWORD_MIN_LENGTH)

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        """Validate password strength if provided."""
        if v is None:
            return v
        min_length = settings.PASSWORD_MIN_LENGTH
        if len(v) < min_length:
            raise ValueError(f'Password must be at least {min_length} characters')
        return v
    
# Additional properties stored in DB but not needed in requests #
class UserInDBBase(UserBase):
    """Base schema for users as stored in DB."""
    id: int
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return via API #
class User(UserInDBBase):
    """Schema for user responses"""
    pass

# Additional properties stored in DB #
class UserInDB(UserInDBBase):
    """Schema with password hash (for internal use only)."""
    hashed_password: str

# Schema for user with roles #
class UserWithRoles(User):
    """Schema for user with their roles."""
    roles: List["RoleBase"] = []

# Schema for password change #
class PasswordChange(BaseModel):
    """Schema for password change requests."""
    current_password: str
    new_password: str = Field(..., min_length=settings.PASSWORD_MIN_LENGTH)

    @field_validator('new_password')
    @classmethod 
    def password_strength(cls, v):
        """Validate new password strength."""
        min_length = settings.PASSWORD_MIN_LENGTH
        if len(v) < min_length:
            raise ValueError(f"Password must be at least {min_length} characters")
        return v
    
# Schema for password reset request #
class PasswordResetRequest(BaseModel):
    """Schema for password reset requests."""
    email: EmailStr

# Schema for password reset confirmation #
class PasswordReset(BaseModel):
    """Schema for password reset confirmations."""
    token: str
    new_password: str = Field(..., min_length=settings.PASSWORD_MIN_LENGTH)

    @field_validator('new_password')
    @classmethod
    def password_strength(cls, v):
        """Validate new password strength."""
        min_length = settings.PASSWORD_MIN_LENGTH
        if len(v) < min_length:
            raise ValueError(f"Password must be at least {min_length} characters")
        return v
    
# Avoid circulatr import issues with roles #
from app.schemas.role import RoleBase
UserWithRoles.model_rebuild()