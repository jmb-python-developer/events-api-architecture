"""
Provider API - FastAPI Mock Service for Fever Events
A modern, professional mock service to replace external provider dependency.
"""

import asyncio
import logging
from datetime import datetime

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from .config import settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Create FastAPI app with configuration
app = FastAPI(
    title=settings.api_title,
    description="Mock service to replace external provider dependency",
    version=settings.api_version,
    docs_url="/docs" if settings.env == "development" else None,
    redoc_url="/redoc" if settings.env == "development" else None,
)

# Add CORS middleware for cross-service communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - basic service info."""
    return {
        "service": settings.api_title,
        "status": "running",
        "version": settings.api_version,
        "environment": settings.env,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health")
async def health_check():
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "provider-api-python",
        "environment": settings.env,
        "checks": {"api": "ok", "memory": "ok", "startup": "ok"},
    }
    logger.debug("Health check accessed", **health_data)
    return health_data


@app.get("/actuator/health")
async def actuator_health():
    """Spring Boot style health endpoint for compatibility with existing monitoring"""
    return {
        "status": "UP",
        "components": {
            "ping": {"status": "UP"},
            "diskSpace": {"status": "UP"},
        },
    }


@app.get("ready")
async def readiness_probe():
    """Kubernetes readiness probe endpoint"""
    return {"status": "ready"}


@app.get("liveness")
async def liveness_probe():
    """Kubernetes liveness probe endpoint"""
    return {"status": "alive"}


# Placeholder for XML Events endpoint
@app.get("/events")
async def get_events():
    """Events endpoint - serves XML events"""
    return Response(
        content="<events><message>Events endpoint ready for implementation</message></events>",
        media_type="application/xml",
    )


@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info(
        "Provider API starting up",
        host=settings.host,
        port=settings.port,
        env=settings.env,
        provider_mode=settings.provider_mode,
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information"""
    logger.info("Provider API shutdown")


if __name__ == "__main__":
    logger.info(
        "Starting provider API",
        host=settings.host,
        port=settings.port,
        env=settings.env,
    )

    uvicorn.run(
        "src.provider-api.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=settings.env == "development",
    )
