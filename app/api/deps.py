from typing import Generator, Optional 

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt 
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import oauth2_scheme, decode_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import TokenPayload
from app.core.exceptions import AuthenticationException, AuthorizationException

def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to get the current authenticated user.

    Args:
        db: Database session
        token: JWT token from Authorization header

    Returns:
        User model instance of the authenticated user

    Raises:
        AuthenticationException: If token is invalid or user not found
    """
    try:
        payload = decode_token(token)
        token_data = TokenPayload(**payload)

        # Check token type #
        if token_data.type != "access":
            raise AuthenticationException(detail="Invalid token type")
        
        # Check token expiration #
        if token_data.exp is None:
            raise AuthorizationException(detail="Token has no expiration")
    except (jwt.JWTError, ValidationError):
        raise AuthenticationException(detail="Could not validate credentials")
    
    # Get user from database #
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise AuthenticationException(detail="User not found")
    
    # Check if user is active #
    if not user.is_active:
        raise AuthenticationException(detail="Inactive user")
    
    return user

def get_current_active_user(
        current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get the current active user.

    Args:
        current_user: Authenticated user from get_current_user

    Returns:
        User model instance if active

    Raises: 
        AuthenticationException: If user is inactive 
    """
    if not current_user.is_active:
        raise AuthenticationException(detail="Inactive user")
    return current_user

def get_current_superuser(
        current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to ensure the current user is a superuser.

    Args:
        current_user: Authenticated user from get_current_user

    Returns:
        User model instance if superuser

    Raises:
        AuthorizationException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise AuthorizationException(detail="Not enough permissions")
    return current_user

def get_current_user_with_permission(permission_code: str):
    """
    Factory for dependencies that check if the current user has a specific permission. 

    Args:
        permission_code: Code of the permission to check

    Returns:
        Dependency function that checks for the specified permission
    """
    def check_permission(current_user: User = Depends(get_current_user)) -> User:
        """
        Check if the current user has the rquired permission through their roles.

        Args:
            current_user: Authenticated user from get_current_user

        Returns:
            User model instance if they have the permission 

        Raises:
            AuthorizationException: If user lacks the required permission
        """
        # Check all roles for the required permission #
        for role in current_user.roles:
            for permission in role.permissions:
                if permission.code == permission_code:
                    return current_user
        
        # Superusers always have all permissions #
        if current_user.is_superuser:
            return current_user
        
        raise AuthorizationException(
            detail=f"Not enough permissions. Required: {permission_code}"
        )
    
    return check_permission

def get_current_user_with_role(role_name: str):
    """
    Factory for dependencies that check if the current user has a specific role.

    Args:
        role_name: Name of the role to check 
    
    Returns: 
        Dependency function that checks for the specified role
    """
    def check_role(current_user: User = Depends(get_current_user)) -> User:
        """
        Check if the current user has the required role.

        Args:
            current_user: Authenticated user from get_current_user

        Returns:
            User model instance if they have the role 

        Raises:
            AuthorizationException: If user lacks the required role
        """
        # Check if the user has the specified role #
        if current_user.has_role(role_name) or current_user.is_superuser:
            return current_user
        
        raise AuthorizationException(
            detail=f"Not enough permissions. Required role: {role_name}"
        )
    
    return check_role 