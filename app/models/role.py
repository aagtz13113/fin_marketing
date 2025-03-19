from sqlalchemy import Column, String, Boolean, Table, Integer, ForeignKey
from sqlalchemy import relationship 

from app.db.base import Base, BaseModel

# Association table for many-to-many relationship between roles and permissions #
role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)

class Role(Base, BaseModel):
    """
    Role model for storing role information.

    Attributes:
        name: Role name (unique)
        descriptions: Role description
        is_default: Whether this is a default role assigned to new users 
        permission: Relationship to permissions (many-to-many)
        users: Relationship to users (many-to-many)
    """
    __tablename__ = "roles"

    # Role attributes #
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    # Relationships #
    permissions = relationship(
        "Permission",
        secondary=role_permission,
        back_populates="roles"
    )

    users = relationship(
        "User",
        secondary="user_role",
        back_populates="roles"
    )

    # Organization ownershipt (optional - for organization-specific roles)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    organization = relationship("Organization", back_populates="roles")

    def __repr__(self):
        return f"<Role {self.name}>"