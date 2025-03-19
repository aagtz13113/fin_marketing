from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.core.config import settings
from app.core.exceptions import CustomException
from app.api.v1.router import api_router
from app.db.session import engine, SessionLocal
from financial_marketing.app.db.session import Base

# Configure logging #
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app #
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Add CORS middleware #
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware to track request duration #
@app.middlware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        process_time = time.time() - start_time
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
            headers={"X-Process-Time": str(process_time)},
        )
    
# Custom exception handler #
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Include API router #
app.include_router(api_router, prefix=settings.API_V1_STR)

# Create database tables on startup (for development only - use migrations in production) #
@app.on_event("startup")
async def startup_db_client():
    try: 
        # Create tables if they don't exist #
        # In production, use Alembic migrations #
        if settings.ENVIRONMENT == "development":
            Base.metadata.create_all(bind=engine)
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Application shutdown")

# Root endpoint #
@app.get("/", include_in_schema=False)
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

# Health check endpoint #
@app.get("/health", include_in_schema=False)
async def health_check():
    try:
        # Check database connection #
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "detail": str(e)},
        ) 