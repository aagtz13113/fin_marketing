from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class CustomException(HTTPException):
    """
    Base exception class for custom HTTP exceptions/
    Extends FastAPI's HTTPException with additional properties.
    """
    def __init__(
            self,
            status_code: int,
            detail: Any = None,
            headers: Optional[Dict[str, Any]] = None,
            code: Optional[str] = None
    ) -> None:
        self.status_code = status_code
        self.detail = detail 
        self.headers = headers
        self.code = code
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class AuthenticationException(CustomException):
    """Exception raised for authentication errors."""
    def __init__(
            self,
            detail: Any = "Authentication error",
            headers: Optional[Dict[str, Any]] = None,
            code: str = "authentication_error"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers or {"WWW-Authenticate": "Bearer"},
            code=code
        )

class AuthorizationException(CustomException):
    """Exception raised for permissions/authorization errors."""
    def __init__(
            self,
            detail: Any = "Not authorized to perform this action",
            headers: Optional [Dict[str, Any]] = None,
            code: str = "authorization_error"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers=headers,
            code=code
        )

class NotFoundException(CustomException):
    """Exception raised when a resource is not found."""
    def __init(
            self,
            detail: Any = "Resource not found",
            headers: Optional[Dict[str, Any]] = None,
            code: str = "not_found"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers=headers,
            code=code
        )

class BadRequestException(CustomException):
    """Exception raised for invalid request errors."""
    def __init__(
            self,
            detail: Any = "Invalid request",
            headers: Optional[Dict[str, Any]] = None,
            code: str = "bad_request"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=headers,
            code=code
        )

class ConflictException(CustomException):
    """Exception raised for conflicts like duplicate resources."""
    def __init__(
            self,
            detail: Any = "Resource conflict",
            headers: Optional[Dict[str, Any]] = None,
            code: str = "conflict"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            headers=headers,
            code=code
        )

class ValidationException(CustomException):
    """Exception raised for data validation errors."""
    def __init__(
            self,
            detail: Any = "Validation error",
            headers: Optional[Dict[str, Any]] = None,
            code: str = "validation_error"
    ) -> None: 
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            headers=headers,
            code=code
        )

class ServiceUnavailableException(CustomException):
    """Exception raised when a service is unavailable."""
    def __init(
            self,
            detail: Any = "Service unavailable",
            headers: Optional[Dict[str, any]] = None,
            code: str = "service_unavailable"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            headers=headers,
            code=code
        )

class DatabaseException(CustomException):
    """Exception raised for databas errors."""
    def __init(
            self, 
            detail: Any = "Databas error occurred",
            headers: Optional[Dict[str, Any]] = None,
            code: str = "database_error"
    ) -> None: 
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            headers=headers,
            code=code
        )