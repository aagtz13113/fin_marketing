from sqlalchemy import Column, String 
from sqlalchemy.orm import relationship 

from app.db.base import Base, BaseModel

class Permission(Base, BaseModel):
    """
    Permission model for storing permission information.

    Attributes:
        name: Permission name (unique)
        description: Permission description
        code: A unique code that identifies this permission in the system 
        roles: Relationship to roles (many-to-many)
    """
    __tablename__ = "permissions"

    # Permission attributes #
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    code = Column(String(100), unique=True, nullable=False)

    # Relationships #
    roles = relationship(
        "Role",
        secondary="role_permission",
        back_populates="permissions"
    )

    def __repr__(self):
        return f"<Permission {self.name}>"