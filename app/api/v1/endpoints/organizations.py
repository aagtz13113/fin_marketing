from typing import Any, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.api.deps import(
    get_current_superuser,
    get_current_user_with_permission,
)
from app.core.exceptions import NotFoundException, ConflictException
from app.db.session import get_db
from app.models.organization import Organization
from app.schemas.organization import(
    Organization as OrganizationSchema,
    OrganizationCreate,
    OrganizationUpdate,
)

router = APIRouter()

@router.get("", response_model=List[OrganizationSchema])
def read_organizations(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(get_current_user_with_permission("org:read")),
) -> Any: 
    """
    Get all organizations.
    """
    # Placeholder implementation - will be expanded later #
    organizations = db.query(Organization).offset(skip).limit(limit).all()
    return organizations 

@router.post("", response_model=OrganizationSchema)
def create_organization(
    *,
    db: Session = Depends(get_db),
    org_in: OrganizationCreate,
    current_user: Any = Depends(get_current_superuser),
) -> Any:
    """
    Create a new organization.
    """
    # Placeholder implementation - will be expanded later #
    # Create new organization #
    organization = Organization(
        name=org_in.name,
        description=org_in.description,
        website=org_in.website,
        is_active=org_in.is_active,
        contact_email=org_in.contact_email,
        contact_phone=org_in.contact_phone,
        address=org_in.address,
    )

    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization 

@router.get("/{org_id}", response_model=OrganizationSchema)
def read_organization(
    *,
    db: Session = Depends(get_db),
    org_id: int = Path(..., gt=0),
    current_user: Any = Depends(get_current_user_with_permission("org:read")),
) -> Any: 
    """
    Get organization by ID.
    """
    # Placeholder implementation - will be expanded later #
    organization = db.query(Organization).filter(Organization.id == org_id).first()
    if not organization:
        raise NotFoundException(detail="Organization not found")
    return organization 

# Additional endpoints for updating, deleting organizations, etc. #
# Will be implemented here #