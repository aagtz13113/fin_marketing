from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship 

from app.db.base import Base, BaseModel

class Organization(Base, BaseModel):
    """
    Organization model for stroing compnay/organization information/

    Attributes:
        name: Organization name
        description: Organization description 
        website: Organization website URL
        is_active: Whether the organization is active
        users: Relationship to users in this organization 
        roles: Relationship to roles defined for this organization 
    """
    __tablename__ = "organizations"

    # Organization attributes #
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    website = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Contact information #
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    address = Column(String(500), nullable=True)

    # Relationships #
    users = relationship("User", back_populates="organization")
    roles = relationship("Role", back_populates="organization")

    def __repr__(self):
        return f"<Organization {self.name}>"