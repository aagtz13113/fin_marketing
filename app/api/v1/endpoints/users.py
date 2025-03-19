from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.api.deps import(
    get_current_user,
    get_current_superuser,
    get_current_user_with_permission
)
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import (
    NotFoundException,
    BadRequestException,
    ConflictException
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    User as UserSchema,
    UserCreate,
    UserUpdate,
    PasswordChange,
    UserWithRoles,
)

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any: 
    """
    Get current user information.
    """
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update current user information.
    """
    # Check if email is being changed and if it's already in use #
    if user_in.email and user_in.email != current_user.email:
        user_with_email = db.query(User).filter(User.email == user_in.email).first()
        if user_with_email:
            raise ConflictException(detail="Email already registered")
        
    # Update user fields #
    user_data = user_in.dict(exclude_unset=True)

    # Handle password separately #
    if user_data.get("password"):
        hashed_password = get_password_hash(user_data.pop("password"))
        user_data["hashed_password"] = hashed_password

    # Update user attributes #
    for key, value in user_data.items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/change-password")
def change_password(
    *,
    db: Session = Depends(get_db),
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Change current user password.
    """
    # Verify current password #
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise BadRequestException(detail="Incorrect password")
    
    # Update password #
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.add(current_user)
    db.commit()

    return {"msg": "Password updated successfully"}

@router.get("", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Retrieve users. Required superuser privileges.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_current_superuser),
) -> Any: 
    """
    Create new user. Requires superuser privileges.
    """
    # Check if user with this email already exists #
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise ConflictException(detail="Email already registered")
    
    # Create new user #
    user = User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        organization_id=user_in.organization_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    *,
    db: Session = Depends(get_db),
    user_id: int = Path(..., gt=0),
    current_user: User = Depends(get_current_superuser),
) -> Any: 
    """
    Get user by ID. Required superuser privileges.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException(detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int = Path(..., gt=0),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Update a user. Requires superuser privileges.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException(detail="User not found")
    
    # Check if email is being changed and if it's already in use #
    if user_in.email and user_in.email != user.email:
        user_with_email = db.query(User).filter(User.email == user_in.email).first()
        if user_with_email:
            raise ConflictException(detail="Email already registered")
        
    # Update user fields #
    user_data = user_in.model_dump(exclude_unset=True)

    # Handle password separately #
    if user_data.get("password"):
        hashed_password = get_password_hash(user_data.pop("password"))
        user_data["hashed_password"] = hashed_password

    # Update user attributes #
    for key, value in user_data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int = Path(..., gt=0),
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Delete a user. Requires superuser privileges.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException(detail="User not found")
    
    # Don't allow deleting your own account #
    if user.id == current_user.id:
        raise BadRequestException(detail="Cannt delete your own account")
    
    db.delete(user)
    db.commit()

    return {"msg": "User deleted successfully"}