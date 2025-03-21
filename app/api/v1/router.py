from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, roles, organizations

# Create main API router #
api_router = APIRouter()

# Include routers from endpoint modules #
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])