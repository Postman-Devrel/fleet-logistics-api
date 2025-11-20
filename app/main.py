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

@app.post("/seed")
def seed_database():
    """Seed the database with fake data. Only run this once!"""
    try:
        from faker import Faker
        from datetime import datetime, timedelta
        import random
        from app.database.config import SessionLocal
        from app.models.models import Organization, Vehicle, Driver, Location, Route, Delivery, MaintenanceRecord, FuelLog, Incident, GPSTracking

        # Initialize Faker
        fake = Faker()
        Faker.seed(42)
        random.seed(42)

        # Create database session
        db = SessionLocal()

        messages = []

        try:
            # Check if already seeded
            org_count = db.query(Organization).count()
            if org_count > 0:
                return {
                    "status": "warning",
                    "message": f"Database already contains {org_count} organizations. Seeding skipped to avoid duplicates.",
                    "suggestion": "Delete existing data first if you want to re-seed"
                }

            messages.append("Starting database seeding...")

            # Seed organizations
            messages.append("Creating 3 organizations...")
            orgs = []
            for name in ["Swift Logistics Inc", "National Transport Co", "Premier Freight Services"]:
                org = Organization(
                    name=name,
                    email=fake.company_email(),
                    phone=fake.phone_number(),
                    address=fake.address().replace('\n', ', '),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(365, 1825))
                )
                orgs.append(org)
                db.add(org)
            db.commit()
            messages.append(f"Created {len(orgs)} organizations")

            # Seed vehicles (simplified for endpoint - just create a few for demo)
            messages.append("Creating 50 vehicles...")
            vehicles = []
            for i in range(50):
                vehicle = Vehicle(
                    organization_id=random.choice(orgs).id,
                    vin=''.join(random.choices('ABCDEFGHJKLMNPRSTUVWXYZ0123456789', k=17)),
                    make=random.choice(["Ford", "Chevrolet", "Freightliner"]),
                    model="Transit",
                    year=random.randint(2015, 2024),
                    license_plate=f"{fake.random_letter().upper()}{fake.random_letter().upper()}{random.randint(1000, 9999)}",
                    vehicle_type=random.choice(["cargo_van", "box_truck", "semi_truck"]),
                    capacity_kg=random.choice([1000, 5000, 10000]),
                    status="active",
                    current_mileage=random.uniform(10000, 200000)
                )
                vehicles.append(vehicle)
                db.add(vehicle)
            db.commit()
            messages.append(f"Created {len(vehicles)} vehicles")

            db.close()

            return {
                "status": "success",
                "message": "Database seeded successfully with basic data!",
                "details": messages,
                "note": "Created organizations and vehicles. For full data set with 1000 deliveries, run scripts/seed_data.py directly."
            }

        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    except Exception as e:
        logger.exception("Seeding error")
        return {
            "status": "error",
            "message": str(e)
        }
