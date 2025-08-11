"""
Health check endpoints
"""
from fastapi import APIRouter, Depends
from datetime import datetime
import time
import asyncio
import psutil
import os

from app.core.config import get_settings, Settings
from app.api.models.common import HealthCheck, HealthStatus, ServiceHealth, SuccessResponse

router = APIRouter()

# Store startup time
startup_time = time.time()

async def check_database_health(settings: Settings) -> ServiceHealth:
    """Check database connectivity"""
    try:
        # TODO: Implement actual database health check
        # For now, just simulate a quick check
        start_time = time.time()
        await asyncio.sleep(0.01)  # Simulate DB query
        response_time = (time.time() - start_time) * 1000
        
        return ServiceHealth(
            status=HealthStatus.HEALTHY,
            response_time_ms=response_time
        )
    except Exception as e:
        return ServiceHealth(
            status=HealthStatus.UNHEALTHY,
            error=str(e)
        )

async def check_redis_health(settings: Settings) -> ServiceHealth:
    """Check Redis connectivity"""
    try:
        # TODO: Implement actual Redis health check
        # For now, just simulate a quick check
        start_time = time.time()
        await asyncio.sleep(0.005)  # Simulate Redis ping
        response_time = (time.time() - start_time) * 1000
        
        return ServiceHealth(
            status=HealthStatus.HEALTHY,
            response_time_ms=response_time
        )
    except Exception as e:
        return ServiceHealth(
            status=HealthStatus.UNHEALTHY,
            error=str(e)
        )

async def check_ddgs_health() -> ServiceHealth:
    """Check DDGS service availability"""
    try:
        # TODO: Implement actual DDGS health check
        # For now, just simulate a check
        start_time = time.time()
        await asyncio.sleep(0.1)  # Simulate external service check
        response_time = (time.time() - start_time) * 1000
        
        return ServiceHealth(
            status=HealthStatus.HEALTHY,
            response_time_ms=response_time
        )
    except Exception as e:
        return ServiceHealth(
            status=HealthStatus.DEGRADED,
            error=str(e)
        )

async def check_ai_services_health(settings: Settings) -> ServiceHealth:
    """Check AI services (Gemini) availability"""
    try:
        if not settings.gemini_api_key:
            return ServiceHealth(
                status=HealthStatus.DEGRADED,
                error="API key not configured"
            )
        
        # TODO: Implement actual AI service health check
        start_time = time.time()
        await asyncio.sleep(0.2)  # Simulate AI service check
        response_time = (time.time() - start_time) * 1000
        
        return ServiceHealth(
            status=HealthStatus.HEALTHY,
            response_time_ms=response_time
        )
    except Exception as e:
        return ServiceHealth(
            status=HealthStatus.DEGRADED,
            error=str(e)
        )

@router.get("/", response_model=SuccessResponse)
async def health_check(settings: Settings = Depends(get_settings)):
    """
    Basic health check endpoint
    Returns overall system health status
    """
    current_time = time.time()
    uptime = int(current_time - startup_time)
    
    # Check individual services
    services = {}
    
    # Core services (required)
    try:
        services["database"] = await check_database_health(settings)
        services["redis"] = await check_redis_health(settings)
    except Exception as e:
        services["core"] = ServiceHealth(
            status=HealthStatus.UNHEALTHY,
            error=f"Core services check failed: {e}"
        )
    
    # Optional services (can be degraded)
    services["ddgs"] = await check_ddgs_health()
    services["ai_services"] = await check_ai_services_health(settings)
    
    # Determine overall status
    core_services_healthy = all(
        service.status == HealthStatus.HEALTHY 
        for key, service in services.items() 
        if key in ["database", "redis", "core"]
    )
    
    if core_services_healthy:
        # Check if any optional services are down
        optional_services_status = [
            service.status for key, service in services.items() 
            if key in ["ddgs", "ai_services"]
        ]
        
        if any(status == HealthStatus.UNHEALTHY for status in optional_services_status):
            overall_status = HealthStatus.DEGRADED
        else:
            overall_status = HealthStatus.HEALTHY
    else:
        overall_status = HealthStatus.UNHEALTHY
    
    health_data = HealthCheck(
        status=overall_status,
        version=settings.version,
        uptime_seconds=uptime,
        services={name: service.status for name, service in services.items()}
    )
    
    return SuccessResponse(
        success=True,
        message=f"System is {overall_status.value}",
        data=health_data
    )

@router.get("/detailed", response_model=SuccessResponse)
async def detailed_health_check(settings: Settings = Depends(get_settings)):
    """
    Detailed health check with service information
    """
    current_time = time.time()
    uptime = int(current_time - startup_time)
    
    # System information
    system_info = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "process_id": os.getpid(),
        "python_version": f"{psutil.sys.version_info.major}.{psutil.sys.version_info.minor}.{psutil.sys.version_info.micro}"
    }
    
    # Check all services with detailed information
    services_detail = {
        "database": await check_database_health(settings),
        "redis": await check_redis_health(settings),
        "ddgs": await check_ddgs_health(),
        "ai_services": await check_ai_services_health(settings)
    }
    
    # Determine overall status
    core_healthy = all(
        service.status == HealthStatus.HEALTHY
        for key, service in services_detail.items()
        if key in ["database", "redis"]
    )
    
    if core_healthy:
        optional_unhealthy = any(
            service.status == HealthStatus.UNHEALTHY
            for key, service in services_detail.items()
            if key in ["ddgs", "ai_services"]
        )
        overall_status = HealthStatus.DEGRADED if optional_unhealthy else HealthStatus.HEALTHY
    else:
        overall_status = HealthStatus.UNHEALTHY
    
    detailed_data = {
        "status": overall_status,
        "version": settings.version,
        "uptime_seconds": uptime,
        "system": system_info,
        "services": services_detail,
        "configuration": {
            "debug_mode": settings.debug,
            "ddgs_enabled": settings.ddgs_enabled,
            "max_text_length": settings.max_text_length,
            "max_file_size": settings.max_file_size // (1024 * 1024)  # Convert to MB
        }
    }
    
    return SuccessResponse(
        success=True,
        message=f"Detailed health check - System is {overall_status.value}",
        data=detailed_data
    )

@router.get("/ready")
async def readiness_check(settings: Settings = Depends(get_settings)):
    """
    Kubernetes readiness probe
    Returns 200 if ready to serve traffic, 503 if not
    """
    try:
        # Check essential services only
        db_health = await check_database_health(settings)
        redis_health = await check_redis_health(settings)
        
        if (db_health.status == HealthStatus.HEALTHY and 
            redis_health.status == HealthStatus.HEALTHY):
            return {"status": "ready"}
        else:
            from fastapi import HTTPException
            raise HTTPException(status_code=503, detail="Service not ready")
    
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Service not ready")

@router.get("/live")
async def liveness_check():
    """
    Kubernetes liveness probe
    Simple endpoint that returns 200 if application is alive
    """
    return {"status": "alive", "timestamp": datetime.now().isoformat()}