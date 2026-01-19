import logging
import logging.config
import os
from pathlib import Path
import time
from typing import Callable
from fastapi import Request, Response
import json
from datetime import datetime

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Basic logging configuration
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            "logs/api.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
    ]
)

# Create a logger instance
logger = logging.getLogger("app")

# Request logging middleware
async def log_requests(request: Request, call_next: Callable) -> Response:
    start_time = time.time()
    
    # Skip logging for health checks
    if request.url.path == "/api/v1/health":
        return await call_next(request)
    
    # Log request
    logger.info(
        "Request received",
        extra={
            "props": {
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client": f"{request.client.host}:{request.client.port}",
                "user_agent": request.headers.get("user-agent"),
            }
        },
    )
    
    try:
        # Process request
        response = await call_next(request)
        
        # Calculate response time
        process_time = (time.time() - start_time) * 1000
        
        # Log response
        logger.info(
            "Request completed",
            extra={
                "props": {
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "response_time_ms": round(process_time, 2),
                }
            },
        )
        
        # Add response time header
        response.headers["X-Response-Time"] = f"{process_time:.2f}ms"
        
        return response
        
    except Exception as e:
        # Log the exception
        logger.error(
            "Request failed",
            exc_info=True,
            extra={
                "props": {
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e),
                }
            },
        )
        raise
