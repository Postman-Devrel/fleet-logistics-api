from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from app.database.config import engine, Base
from app.routers import (
    organizations,
    vehicles,
    drivers,
    locations,
    routes,
    deliveries,
    maintenance,
    fuel,
    incidents,
    gps
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fleet Logistics API",
    description="A comprehensive fleet management and logistics tracking system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        logger.error("Make sure DATABASE_URL environment variable is set correctly")
        # Don't crash the app, just log the error
        # This allows the app to start even if DB isn't ready yet

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(organizations.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(locations.router)
app.include_router(routes.router)
app.include_router(deliveries.router)
app.include_router(maintenance.router)
app.include_router(fuel.router)
app.include_router(incidents.router)
app.include_router(gps.router)

@app.get("/")
def root():
    return {
        "message": "Fleet Logistics API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    db_status = "unknown"
    db_url = os.getenv("DATABASE_URL", "not_set")

    try:
        # Try to connect to database
        with engine.connect() as conn:
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "database_url_configured": db_url != "not_set"
    }
