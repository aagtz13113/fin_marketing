from datetime import datetime, timedelta 
from typing import Any, Dict, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from app.core.config import settings

# Password hashing context #
pwd_context = CryptContext(schemes=["brcrypt"], deprecated="auto")

# OAuth2 scheme for token-based authentication #
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for a user.

    Args:
        subject: User identifier (typically a User ID)
        expires_delta: Token expiration time (optional)

    Returns:
        JWT token as a string
    """
    if expires_delta:
        expire = datetime.now() + expires_delta
    else: 
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # JWT claims #
    to_encode = {
        "exp": expire,
        "iat": datetime.now(),
        "sub": str(subject),
        "type": "access"
    }

    # Create and return the encoded JWT #
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any]) -> str:
    """
    Create a JWT refresh token for a user/

    Args:
        subject: User identifier (typically user ID)

    Returns: 
        JWT token as a string 
    """
    expire = datetime.now() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )

    # JWT Claims #
    to_encode = {
        "exp": expire,
        "iat": datetime.now(),
        "sub": str(subject),
        "type": "refresh"
    }

    # Create and return the encoded JWT #
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain_password: Password in plain text
        hashed_password: Hashed password from database

    Returns:
        True if password matched hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a hash for a password.

    Args:
        password: Password in plain text

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token to decode

    Returns:
        Dict containing token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )