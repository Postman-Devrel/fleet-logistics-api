from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fleet Logistics API",
    description="A comprehensive fleet management and logistics tracking system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

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
    return {"status": "healthy"}
