from fastapi import HTTPException, status
from typing import Any, Dict, Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class BaseAPIException(HTTPException):
    status_code: int
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None

    def __init__(self, **kwargs: Any):
        super().__init__(
            status_code=self.status_code,
            detail={
                "success": False,
                "message": self.message,
                "error_code": self.error_code,
                "details": kwargs.get("details") or self.details
            }
        )


class NotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "not_found"
    message = "The requested resource was not found"


class ValidationError(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "validation_error"
    message = "Validation error"


class InternalServerError(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "internal_server_error"
    message = "Internal server error"


def register_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail.get("message") if isinstance(exc.detail, dict) else str(exc.detail),
                "error_code": exc.detail.get("error_code", "http_error"),
                "details": exc.detail.get("details")
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        # In production, you might want to log this to an error tracking service
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "An unexpected error occurred",
                "error_code": "internal_server_error",
                "details": None
            }
        )
