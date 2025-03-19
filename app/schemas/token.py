from typing import Optional 
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """Schema for token payload."""
    sub: Optional[str] = None
    exp: Optional[str] = None
    type: Optional[str] = None

class TokenRefresh(BaseModel):
    """Schema for token refresh requests."""
    refresh_token: str

class Login(BaseModel):
    """Schema for login requests."""
    email: EmailStr
    password: str