from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, Table 
from sqlalchemy.orm import relationship

from app.db.base import Base, BaseModel

# Association table for many-to-many relationship between users and roles #
user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

class User(Base, BaseModel):
    """
    User model for storing user information and authentication data.

    Attributes:
        email: User's email address (unique identifier)
        first_name: User's first name 
        last_name: User's last name
        hashed_password: Securely hashed password
        is_active: Whether the user account is active 
        is_superuser: Whether the user has superuser privileges 
        organization_id: ID of the organization the user belongs to
    """
    __tablename__ = "users"

    # User identification and authentication #
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    hashed_password = Column(String, nullable=False)

    # User status and permissions #
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    # Organization relationship (many-to-one) #
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    organization = Column(Boolean, default=False, nullable=False)

    # Role relationship (many-to-many) #
    roles = relationship(
        "Role",
        secondary=user_role,
        back_populates="users"
    )

    # Email verification #
    is_email_verified = Column(Boolean, default=False, nullable=False)
    email_verification_token = Column(String, nullable=True)

    # Password reset # 
    password_reset_token = Column(String, nullable=True)
    password_reset_expires = Column(String, nullable=True)

    # Last login tracking #
    last_login = Column(String, nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"
    
    @property
    def full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def has_role(self, role_name: str) -> bool:
        """Check if the user has a specific role by name"""
        return any(role.name == role_name for role in self.roles)