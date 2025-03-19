# Financial Marketing Compliance Platform

A sophisticated platform that automates the regulatory review process for financial institutions' marketing materials, using AI/LLM technology to analyze marketing content against SEC, FINRA, and other regulatory standards.

## Project Overview

This platform serves as a comprehensive solution for financial compliance teams, enabling them to:

- Automatically analyze marketing content for compliance issues
- Map specific regulatory requirements to content problems
- Track submission status to regulatory agencies
- Generate alternative compliant content suggestions
- Provide analytics on compliance rates and processing time

## Current Status

The project is in active development with the following modules:

### Completed
- ✅ **Authentication & User Management Backend**
  - User model with authentication details
  - JWT token-based authentication
  - Role-based access control (RBAC) system
  - Organization structure for multi-tenancy
  - API endpoints for user management

### In Progress
- 🔄 **Database Migrations**
  - Alembic configuration
  - Initial migration scripts

### Pending Development
- 📝 **Document Processing**
  - Secure document upload and validation
  - Text extraction and preprocessing
  - Document version control
  - Format conversion

- 📝 **Compliance Analysis**
  - Gumloop LLM integration for analysis
  - Content classification
  - Regulatory code mapping
  - Alternative content suggestions

- 📝 **Submission Management**
  - Submission status tracking
  - Agency communication
  - Feedback management
  - Historical submission data

- 📝 **Analytics & Reporting**
  - Performance metrics
  - Compliance success rate tracking
  - Processing time analytics
  - Custom report generation

## Technical Architecture

The application is built with:

- Backend: Python FastAPI
- Database: PostgreSQL with SQLAlchemy ORM
- Authentication: JWT tokens
- API Documentation: OpenAPI (Swagger)
- LLM Integration: Gumloop platform

## Project Structure

```
financial_marketing/
│
├── app/                              # Main application package
│   ├── main.py                       # FastAPI application entry point
│   ├── core/                         # Core configuration modules
│   │   ├── config.py                 # Environment & app configuration
│   │   ├── security.py               # Security utilities (JWT, hashing)
│   │   └── exceptions.py             # Custom exception handlers
│   │
│   ├── db/                           # Database related code
│   │   ├── session.py                # Database session management
│   │   └── base.py                   # Base model class
│   │
│   ├── models/                       # SQLAlchemy ORM models
│   │   ├── user.py                   # User model
│   │   ├── role.py                   # Role model
│   │   ├── permission.py             # Permission model
│   │   └── organization.py           # Organization model
│   │
│   ├── schemas/                      # Pydantic schemas
│   │   ├── user.py                   # User schemas
│   │   ├── role.py                   # Role schemas
│   │   ├── permission.py             # Permission schemas
│   │   ├── organization.py           # Organization schemas
│   │   └── token.py                  # Authentication token schemas
│   │
│   ├── api/                          # API routes
│   │   ├── deps.py                   # Dependency injection
│   │   └── v1/                       # API version 1
│   │       ├── endpoints/            # Endpoint modules
│   │       │   ├── auth.py           # Authentication endpoints
│   │       │   ├── users.py          # User management endpoints
│   │       │   ├── roles.py          # Role management endpoints
│   │       │   └── organizations.py  # Organization management
│   │       └── router.py             # API router
│   │
│   └── services/                     # Business logic services (pending)
│
├── tests/                            # Tests directory (pending)
│
├── alembic/                          # Alembic migration files (pending)
│
├── requirements.txt                  # Project dependencies
└── .env.example                      # Example environment variables
```

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- Virtual environment (recommended)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd financial_marketing
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example` and configure your environment variables

5. Run the application
```bash
uvicorn app.main:app --reload
```

6. Access the API documentation at `http://localhost:8000/api/v1/docs`

## Next Steps

The following items are planned for immediate development:

1. **Database Migrations**
   - Set up Alembic for database migrations
   - Create initial migration scripts
   - Add seed data for default roles and permissions

2. **User Management Completion**
   - Implement email verification
   - Complete password reset functionality
   - Add multi-factor authentication

3. **Document Processing Module**
   - File upload endpoints with validation
   - Document storage integration
   - Text extraction and preprocessing
   - Document version control

4. **Testing**
   - Unit tests for authentication flows
   - Integration tests for API endpoints
   - User role and permission testing

5. **Gumloop Integration**
   - Design integration architecture
   - Create service layer for Gumloop communication
   - Implement compliance check workflows

## API Documentation

Once the server is running, you can access detailed API documentation at:

- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## Environment Variables

Key environment variables required for the application:

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=Financial Marketing Compliance Platform
ENVIRONMENT=development

# Security
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=11520  # 8 days
REFRESH_TOKEN_EXPIRE_MINUTES=43200  # 30 days

# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=financial_marketing
POSTGRES_PORT=5432

# Admin User
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin_password

# CORS
CORS_ORIGINS=http://localhost,http://localhost:8080

## Contributing

For development guidelines and contribution workflow, please refer to the project's contribution guidelines (pending).

## License

This project is licensed under [License Name] - see the LICENSE file for details.
