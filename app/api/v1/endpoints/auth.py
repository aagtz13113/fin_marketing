from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import(
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    decode_token,
)
from app.core.config import settings
from app.core.exceptions import (
    AuthenticationException,
    NotFoundException,
    BadRequestException,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token, TokenRefresh, Login
from app.schemas.user import (
    UserCreate,
    PasswordReset,
    PasswordResetRequest,
    User as UserSchema,
)
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/login", response_model=Token)
def login_acces_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an acess token for future requests. 

    Args:
        db: Database session 
        form_data: OAuth2 form containing username (email) and password

    Returns: 
        Access and refresh tokens  
    """
    # Authenticate the user
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise AuthenticationException(detail="Incorrect email or password")
    
    # Generate tokens #
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minuts=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    # Update last login timestamp #
    user.last_login = datetime.now()
    db.commit()

    return {
        "access_token": create_access_token(
            subject=user.id, expires_delta=access_token_expires
        ),
        "refresh_token": create_refresh_token(subject=user.id),
        "token_type": "bearer",
    }

@router.post("/login/email", response_model=Token)
def login_with_email(
    *,
    db: Session = Depends(get_db),
    login_data: Login,
) -> Any:
    """
    Login endpoint for clients that don't support OAuth2 form.

    Args:
        db: Database session
        login_data: Email and password

    Returns:
        Access and refresh tokenss
    """
    # Authenticate the user #
    user = authenticate_user(db, email=login_data.email, password=login_data.password)
    if not user:
        raise AuthenticationException(detail="Incorrect email or password")
    
    # Generate tokens #
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Update last login timestamp #
    user.last_login = datetime.now()
    db.commit()

    return {
        "access_token": create_access_token(
            subject=user.id, expires_delta=access_token_expires
        ),
        "refresh_token": create_refresh_token(subject=user.id),
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=Token)
def refresh_token(
    db: Session = Depends(get_db),
    refresh_token_data: TokenRefresh = Body(...),
) -> Any:
    """
    Refresh access token using refresh token.

    Args:
        db: Databas session
        refresh_token_data: Refresh token

    Returns:
        New access and refresh tokens
    """
    try:
        # Decode and validate refresh token #
        payload = decode_token(refresh_token_data.refresh_token)

        # Check token type #
        if payload.get("type") != "refresh":
            raise AuthenticationException(detail="Invalid token type")
        
        # Get user from database #
        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationException(detail="Invalid token")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise AuthenticationException(detail="User not found")
        
        # Check if user is active #
        if not user.is_active:
            raise AuthenticationException(detail="Inactive user")
        
        # Generate new tokens #
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        return {
            "access_token": create_access_token(
                subject=user.id, expires_delta=access_token_expires
            ),
            "refresh_token": create_refresh_token(subject=user.id),
            "token_type": "bearer"
        }
    except Exception as e:
        raise AuthenticationException(detail="Invalid refresh token")
    
@router.post("/test-token", response_model=UserSchema)
def test_token(current_user: User = Depends(get_current_user)) -> Any:
    """
    Test access token validity.

    Args: 
        current_user: Current authenticated user

    Returns:
        User information
    """
    return current_user

@router.post("/password-reset-request")
def request_password_request(
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db),
) -> Any:
    """
    Request a password reset token.

    Args:
        reset_request: Email address for reset
        db: Database session 

    Returns: 
        Success message
    """
    user = db.query(User).filter(User.email == reset_request.email).first()

    # Always return a success response even if user not found (security) #
    if not user:
        return {"msg": "If this email is registered, a password reset link has been sent"}

    # Generate password reset token 
    # Note: In a production system, you would:
    # 1. Create a time-limited token
    # 2. Store it in the user record
    # 3. Send an email with a link containing the token
    # Here we'll just generate it (implementation would depend on your email service)
    # 
    # Example: Set a token valid for 24 hours
    # token = create_access_token(
    #     subject=f"reset:{user.id}", expires_delta=timedelta(hours=24)
    # ) 
    # user.password_reset_token = token
    # user.password_reset_expires = datetime.now() + timedelta(hours=24)
    # db.commit()

    # In a real app, you would send an email with the reset link 
    # send_reset_password_email(email=user.email, token=token)

    return {"msg": "If this email is registered, a password reset link has been sent"}

@router.post("/password-reset")
def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db),
) -> Any:
    """
    Reset a user's password using a reset token.

    Args: 
        reset_data: Token and new password
        db: Database session 

    Returns:
        Success message
    """
    # In a real system, you would:
    # 1. Verify the token
    # 2. Check if it's expired
    # 3. Update the password

    # Example implementation (simplified)
    try:
        # Decode token (would validate with a special key/flow in production)
        # payload = decode_token(reset_data.token)
        # if not payload.get("sub", "").startswith("reset:"):
        #     raise BadRequestException(detail="Invalid token")
        
        # Extrace user ID from subject 
        # user_id = payload.get("sub").split(":", 1)[1]
        # user = db.query(User).filter(User.id == user_id).first()

        # if not user or user.password_reset_token != reset_data.token:
        #     raise BadRequestException(detail="Invalid token")

        # Check if token is expired
        # now = datetime.now()
        # if not user.password_reset_expires or user.password_reset_expries < now:
        #     raise BadRequestException(detail="Token expired")

        # Update password
        # user.hashed_password = get_password_hash(reset_data.new_password)
        # user.password_reset_token = None
        # user.password_reset_expires = None
        # db.commit()

        # This is a stub for now - will be implemented fully later
        return {"msg": "Password reset successfully"}
    except Exception:
        raise BadRequestException(detail="Invalid or expired token")
    
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Args:
        db: Database session
        email: User's email
        password: User's password

    Returns:
        User object if authentication successful, None otherwise
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password): 
        return None
    return user 