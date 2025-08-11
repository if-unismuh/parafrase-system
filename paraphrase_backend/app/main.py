"""
Main FastAPI application
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import time
import logging
import traceback

from app.core.config import get_settings
from app.core.exceptions import ParaphraseAPIException
from app.api.router import api_router
from app.api.models.common import ErrorResponse, ErrorDetail

# Get settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add middleware
if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )

# Add trusted host middleware in production
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure this properly in production
    )

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f"{process_time:.4f}")
    return response

# Exception handlers
@app.exception_handler(ParaphraseAPIException)
async def api_exception_handler(request: Request, exc: ParaphraseAPIException):
    """Handle custom API exceptions"""
    logger.error(f"API Exception: {exc.code} - {exc.message}", extra={"details": exc.details})
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            success=False,
            message="Request failed",
            error=ErrorDetail(
                code=exc.code,
                message=exc.message,
                details=exc.details
            )
        ).dict()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    logger.error(f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            success=False,
            message="Validation failed",
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Invalid input data",
                details={"errors": exc.errors()}
            )
        ).dict()
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            message="HTTP error",
            error=ErrorDetail(
                code=f"HTTP_{exc.status_code}",
                message=str(exc.detail),
                details={"status_code": exc.status_code}
            )
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    # Don't expose internal errors in production
    if settings.debug:
        error_details = {
            "type": type(exc).__name__,
            "traceback": traceback.format_exc()
        }
        message = str(exc)
    else:
        error_details = None
        message = "Internal server error"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            success=False,
            message="Internal server error",
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message=message,
                details=error_details
            )
        ).dict()
    )

# Include routers
app.include_router(api_router, prefix=settings.api_v1_prefix)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info(f"Starting {settings.app_name} v{settings.version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Environment: {settings.__class__.__name__}")
    
    # Initialize services here
    # e.g., database connections, cache, etc.

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("Shutting down application")
    
    # Cleanup resources here
    # e.g., close database connections, cache, etc.

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "docs": "/docs" if settings.debug else "Documentation not available in production",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )