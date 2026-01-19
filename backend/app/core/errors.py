from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import Any, Dict, List, Optional, Union
import logging
import traceback

logger = logging.getLogger(__name__)

class APIError(Exception):
    """
    Base class for API errors with HTTP status codes and error details.
    """
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "An unexpected error occurred",
        error_code: Optional[str] = None,
        details: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code or f"HTTP_{status_code}"
        self.details = details
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the error to a dictionary for JSON serialization."""
        error_dict = {
            "success": False,
            "error": self.message,
            "error_code": self.error_code,
        }
        if self.details is not None:
            error_dict["details"] = self.details
        return error_dict

async def handle_api_error(request: Request, exc: APIError) -> JSONResponse:
    """
    Handle API errors and return a consistent JSON response.
    """
    logger.error(
        f"API Error: {exc.message} (status_code={exc.status_code}, error_code={exc.error_code})"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )

async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle FastAPI HTTP exceptions and return a consistent JSON response.
    """
    error_code = f"HTTP_{exc.status_code}"
    logger.warning(
        f"HTTP Exception: {exc.detail} (status_code={exc.status_code}, error_code={error_code})"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": str(exc.detail),
            "error_code": error_code,
        },
    )

async def handle_validation_error(
    request: Request, exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    """
    Handle request validation errors and return a detailed error response.
    """
    errors = []
    
    if isinstance(exc, RequestValidationError):
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
            errors.append({
                "field": field or "body",
                "message": error["msg"],
                "type": error["type"],
            })
    elif isinstance(exc, ValidationError):
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            errors.append({
                "field": field,
                "message": error["msg"],
                "type": error["type"],
            })
    
    logger.warning(f"Validation error: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation Error",
            "error_code": "VALIDATION_ERROR",
            "details": errors,
        },
    )

async def handle_unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unhandled exceptions and return a generic error response.
    Logs the full stack trace for debugging purposes.
    """
    error_id = f"err_{hash(exc) & 0xFFFFFFFF:08x}"
    logger.error(
        f"Unhandled exception (ID: {error_id}): {str(exc)}\n"
        f"Path: {request.method} {request.url}\n"
        f"Stack trace:\n{traceback.format_exc()}"
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "An unexpected error occurred",
            "error_code": "INTERNAL_SERVER_ERROR",
            "error_id": error_id,
            "message": "Please contact support with the error ID if the problem persists.",
        },
    )

def register_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI application.
    
    Args:
        app: The FastAPI application instance
    """
    # Register custom exception handlers
    app.add_exception_handler(APIError, handle_api_error)
    app.add_exception_handler(HTTPException, handle_http_exception)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(ValidationError, handle_validation_error)
    app.add_exception_handler(Exception, handle_unhandled_exception)
    
    logger.info("Exception handlers registered")
    
    return app
