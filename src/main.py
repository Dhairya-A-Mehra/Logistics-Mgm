from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api.routers.analytics import router as analytics_router
from .database import engine, Base
from .api.routers import admin, ai_router,auth,delivery
from .config import settings

# Import all models to register them with Base
from .models import (
    Customer,
    Warehouse,
    Vehicle,
    Order,
    Shipment,
    Inventory,
    VehicleTelemetry,
    FuelPrice,
    PackagingType,
    Document,
    AgentAuditLog,
)
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup: Create database tables (only if DB is accessible)
    try:
        logger.info("Attempting to create database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.warning(f"Could not create database tables at startup: {e}")
        logger.warning("Tables will be created on first database access")

    yield

    # Shutdown: Clean up resources
    logger.info("Application shutting down")


app = FastAPI(
    title="Logimas API",
    version="1.0.0",
    description="Logistics Management System API with JWT Authentication",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(
    admin.router, prefix="/api/v1/admin", tags=["Admin - User Management"]
)
app.include_router(analytics_router, prefix="/api/v1", tags=["Analytics"])
app.include_router(delivery.router, prefix="/api/v1/delivery", tags=["Delivery"])
app.include_router(ai_router.router, prefix="/ai", tags=["AI"])


@app.get("/api/health", tags=["Health Check"])
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}


@app.get("/api/health/db", tags=["Health Check"])
def database_health_check():
    """Database health check endpoint"""
    from sqlalchemy import text
    from .database import engine

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "message": "Database connection successful",
            "database": "connected",
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "error",
            "message": "Database connection failed",
            "database": "disconnected",
            "error": str(e),
        }


# Backwards-compatible alias for analytics summary at /api/v1/analytics/summary
try:
    from .api.routers.analytics import get_analytics_summary as _get_analytics_summary
    from .api.routers.analytics import get_supabase_client as _get_supabase_client
    from fastapi import HTTPException

    @app.get("/api/v1/analytics/summary", tags=["Analytics"])
    def _legacy_analytics_summary():
        """Alias that calls the analytics router logic directly to ensure the legacy path works."""
        try:
            supabase = _get_supabase_client()
        except HTTPException:
            # propagate HTTPException from client factory
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return _get_analytics_summary(supabase)
except Exception:
    # If imports fail, skip adding alias — main router still provides analytics endpoints.
    pass
