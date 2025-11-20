from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from faker import Faker
from datetime import datetime, timedelta
import random
from app.database.config import get_db
from app.models.models import (
    Organization, Vehicle, Driver, Location, Route,
    Delivery, MaintenanceRecord, FuelLog, Incident, GPSTracking
)

router = APIRouter(prefix="/admin", tags=["admin"])

# Configuration
NUM_VEHICLES = 50
NUM_DRIVERS = 60
NUM_LOCATIONS = 100
NUM_ROUTES = 400
NUM_DELIVERIES = 1000
HISTORY_MONTHS = 6

# Vehicle data
VEHICLE_MAKES = ["Ford", "Chevrolet", "Freightliner", "Peterbilt", "Kenworth", "Volvo", "Mercedes-Benz", "RAM"]
VEHICLE_MODELS = {
    "Ford": ["Transit", "F-150", "F-250", "E-Series"],
    "Chevrolet": ["Express", "Silverado 2500", "Silverado 3500"],
    "Freightliner": ["Cascadia", "M2 106", "Sprinter"],
    "Peterbilt": ["579", "389", "567"],
    "Kenworth": ["T680", "W900", "T880"],
    "Volvo": ["VNL", "VNR"],
    "Mercedes-Benz": ["Sprinter", "Actros"],
    "RAM": ["ProMaster", "2500", "3500"]
}
VEHICLE_TYPES = ["cargo_van", "pickup_truck", "box_truck", "semi_truck", "refrigerated_truck"]
LOCATION_TYPES = ["warehouse", "depot", "customer", "distribution_center"]
US_STATES = ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI"]

def generate_vin():
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    return ''.join(random.choice(chars) for _ in range(17))

def generate_tracking_number():
    return f"TRK{random.randint(100000000, 999999999)}"

@router.post("/seed-full")
def seed_database_full(db: Session = Depends(get_db)):
    """Seed the database with complete dataset: 50 vehicles, 1000 deliveries, 6 months history"""

    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    messages = []

    try:
        # Check if already seeded
        org_count = db.query(Organization).count()
        if org_count > 0:
            return {
                "status": "warning",
                "message": f"Database already contains {org_count} organizations. Seeding skipped.",
                "suggestion": "Use /admin/clear endpoint first if you want to re-seed"
            }

        base_date = datetime.utcnow() - timedelta(days=HISTORY_MONTHS * 30)

        # 1. Organizations
        messages.append("Creating 3 organizations...")
        orgs = []
        for name in ["Swift Logistics Inc", "National Transport Co", "Premier Freight Services"]:
            org = Organization(
                name=name,
                email=fake.company_email(),
                phone=fake.phone_number(),
                address=fake.address().replace('\n', ', '),
                created_at=base_date
            )
            orgs.append(org)
            db.add(org)
        db.commit()
        messages.append(f"✓ Created {len(orgs)} organizations")

        # 2. Vehicles
        messages.append(f"Creating {NUM_VEHICLES} vehicles...")
        vehicles = []
        for i in range(NUM_VEHICLES):
            make = random.choice(VEHICLE_MAKES)
            vehicle = Vehicle(
                organization_id=random.choice(orgs).id,
                vin=generate_vin(),
                make=make,
                model=random.choice(VEHICLE_MODELS[make]),
                year=random.randint(2015, 2024),
                license_plate=f"{fake.random_letter().upper()}{fake.random_letter().upper()}{random.randint(1000, 9999)}",
                vehicle_type=random.choice(VEHICLE_TYPES),
                capacity_kg=random.choice([1000, 2000, 5000, 10000, 20000]),
                status=random.choices(["active", "maintenance", "retired"], weights=[0.85, 0.13, 0.02])[0],
                current_mileage=random.uniform(10000, 500000),
                created_at=base_date
            )
            vehicles.append(vehicle)
            db.add(vehicle)
        db.commit()
        messages.append(f"✓ Created {len(vehicles)} vehicles")

        # 3. Drivers
        messages.append(f"Creating {NUM_DRIVERS} drivers...")
        drivers = []
        for i in range(NUM_DRIVERS):
            hire_date = base_date + timedelta(days=random.randint(0, HISTORY_MONTHS * 30))
            driver = Driver(
                organization_id=random.choice(orgs).id,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                license_number=f"DL{random.randint(10000000, 99999999)}",
                license_expiry=datetime.utcnow() + timedelta(days=random.randint(30, 1825)),
                status=random.choices(["active", "inactive", "on_leave"], weights=[0.9, 0.05, 0.05])[0],
                hire_date=hire_date,
                rating=round(random.uniform(3.5, 5.0), 1),
                created_at=hire_date
            )
            drivers.append(driver)
            db.add(driver)
        db.commit()
        messages.append(f"✓ Created {len(drivers)} drivers")

        # 4. Locations
        messages.append(f"Creating {NUM_LOCATIONS} locations...")
        locations = []
        for i in range(NUM_LOCATIONS):
            location = Location(
                organization_id=random.choice(orgs).id,
                name=f"{fake.company()} - {fake.city()}",
                type=random.choice(LOCATION_TYPES),
                address=fake.street_address(),
                city=fake.city(),
                state=random.choice(US_STATES),
                postal_code=fake.zipcode(),
                country="USA",
                latitude=random.uniform(25.0, 48.0),
                longitude=random.uniform(-125.0, -65.0),
                created_at=base_date
            )
            locations.append(location)
            db.add(location)
        db.commit()
        messages.append(f"✓ Created {len(locations)} locations")

        # 5. Routes
        messages.append(f"Creating {NUM_ROUTES} routes...")
        routes = []
        for i in range(NUM_ROUTES):
            origin = random.choice(locations)
            destination = random.choice([loc for loc in locations if loc.id != origin.id])
            scheduled_departure = base_date + timedelta(days=random.randint(0, HISTORY_MONTHS * 30))
            distance_km = random.uniform(50, 2000)
            scheduled_arrival = scheduled_departure + timedelta(hours=distance_km / random.uniform(60, 80))

            status = random.choices(["scheduled", "in_progress", "completed", "cancelled"], weights=[0.1, 0.05, 0.8, 0.05])[0]
            actual_departure = scheduled_departure + timedelta(minutes=random.randint(-30, 60)) if status in ["in_progress", "completed"] else None
            actual_arrival = scheduled_arrival + timedelta(minutes=random.randint(-60, 120)) if status == "completed" else None

            route = Route(
                vehicle_id=random.choice(vehicles).id,
                driver_id=random.choice(drivers).id,
                origin_location_id=origin.id,
                destination_location_id=destination.id,
                scheduled_departure=scheduled_departure,
                actual_departure=actual_departure,
                scheduled_arrival=scheduled_arrival,
                actual_arrival=actual_arrival,
                distance_km=distance_km,
                status=status,
                created_at=scheduled_departure - timedelta(days=random.randint(1, 7))
            )
            routes.append(route)
            db.add(route)
        db.commit()
        messages.append(f"✓ Created {len(routes)} routes")

        # 6. Deliveries
        messages.append(f"Creating {NUM_DELIVERIES} deliveries...")
        for i in range(NUM_DELIVERIES):
            route = random.choice(routes)
            scheduled_delivery = route.scheduled_arrival + timedelta(hours=random.randint(0, 48))

            status_weights = [0.05, 0.1, 0.83, 0.02] if route.status == "completed" else [0.7, 0.2, 0.08, 0.02]
            status = random.choices(["pending", "in_transit", "delivered", "failed"], weights=status_weights)[0]
            actual_delivery = scheduled_delivery + timedelta(hours=random.randint(-12, 24)) if status == "delivered" else None

            delivery = Delivery(
                route_id=route.id,
                location_id=random.choice(locations).id,
                tracking_number=generate_tracking_number(),
                customer_name=fake.name(),
                customer_email=fake.email(),
                customer_phone=fake.phone_number(),
                package_count=random.randint(1, 50),
                weight_kg=random.uniform(1, 1000),
                status=status,
                priority=random.choices(["standard", "express", "urgent"], weights=[0.7, 0.2, 0.1])[0],
                scheduled_delivery=scheduled_delivery,
                actual_delivery=actual_delivery,
                delivery_notes=fake.sentence() if random.random() > 0.7 else None,
                signature_required=random.choice([True, False]),
                created_at=route.created_at
            )
            db.add(delivery)
        db.commit()
        messages.append(f"✓ Created {NUM_DELIVERIES} deliveries")

        # 7. Maintenance Records
        messages.append("Creating maintenance records...")
        maintenance_count = 0
        for vehicle in vehicles:
            for _ in range(random.randint(2, 6)):
                service_date = base_date + timedelta(days=random.randint(0, HISTORY_MONTHS * 30))
                maintenance_type = random.choice(["routine", "repair", "inspection", "emergency"])

                maintenance = MaintenanceRecord(
                    vehicle_id=vehicle.id,
                    maintenance_type=maintenance_type,
                    description=f"{maintenance_type.title()} service",
                    cost=random.uniform(100, 5000),
                    mileage_at_service=vehicle.current_mileage - random.uniform(0, 50000),
                    service_date=service_date,
                    next_service_date=service_date + timedelta(days=random.randint(30, 180)) if maintenance_type == "routine" else None,
                    service_provider=fake.company(),
                    downtime_hours=random.uniform(1, 48) if maintenance_type in ["repair", "emergency"] else random.uniform(0.5, 4),
                    created_at=service_date
                )
                db.add(maintenance)
                maintenance_count += 1
        db.commit()
        messages.append(f"✓ Created {maintenance_count} maintenance records")

        # 8. Fuel Logs
        messages.append("Creating fuel logs...")
        fuel_count = 0
        for vehicle in vehicles:
            for _ in range(random.randint(20, 40)):
                fuel_date = base_date + timedelta(days=random.uniform(0, HISTORY_MONTHS * 30))
                liters = random.uniform(50, 400)
                cost_per_liter = random.uniform(1.2, 2.0)

                fuel_log = FuelLog(
                    vehicle_id=vehicle.id,
                    date=fuel_date,
                    location=f"{fake.city()}, {random.choice(US_STATES)}",
                    liters=liters,
                    cost_per_liter=cost_per_liter,
                    total_cost=liters * cost_per_liter,
                    mileage=vehicle.current_mileage - random.uniform(0, 50000),
                    fuel_type=random.choices(["diesel", "gasoline", "electric"], weights=[0.7, 0.25, 0.05])[0],
                    created_at=fuel_date
                )
                db.add(fuel_log)
                fuel_count += 1
        db.commit()
        messages.append(f"✓ Created {fuel_count} fuel logs")

        # 9. Incidents
        messages.append("Creating incidents...")
        incident_count = 0
        drivers_with_incidents = random.sample(drivers, k=int(len(drivers) * 0.3))
        for driver in drivers_with_incidents:
            for _ in range(random.randint(1, 3)):
                incident_date = base_date + timedelta(days=random.randint(0, HISTORY_MONTHS * 30))
                incident_type = random.choice(["accident", "delay", "damage", "theft", "violation"])
                severity = random.choices(["minor", "moderate", "major", "critical"], weights=[0.5, 0.3, 0.15, 0.05])[0]
                resolved = incident_date < datetime.utcnow() - timedelta(days=7)

                incident = Incident(
                    driver_id=driver.id,
                    incident_type=incident_type,
                    severity=severity,
                    description=fake.sentence(),
                    date=incident_date,
                    location=f"{fake.city()}, {random.choice(US_STATES)}",
                    cost=random.uniform(100, 10000) if incident_type in ["accident", "damage", "theft"] else None,
                    resolved=resolved,
                    resolution_notes=fake.sentence() if resolved else None,
                    created_at=incident_date
                )
                db.add(incident)
                incident_count += 1
        db.commit()
        messages.append(f"✓ Created {incident_count} incidents")

        # 10. GPS Tracking
        messages.append("Creating GPS tracking data...")
        gps_count = 0
        recent_date = datetime.utcnow() - timedelta(days=30)
        for vehicle in random.sample(vehicles, k=min(30, len(vehicles))):
            lat = random.uniform(25.0, 48.0)
            lon = random.uniform(-125.0, -65.0)

            for _ in range(random.randint(50, 200)):
                timestamp = recent_date + timedelta(minutes=random.uniform(0, 30 * 24 * 60))
                lat += random.uniform(-0.1, 0.1)
                lon += random.uniform(-0.1, 0.1)
                lat = max(25.0, min(48.0, lat))
                lon = max(-125.0, min(-65.0, lon))

                gps = GPSTracking(
                    vehicle_id=vehicle.id,
                    timestamp=timestamp,
                    latitude=lat,
                    longitude=lon,
                    speed_kmh=random.uniform(0, 100),
                    heading=random.uniform(0, 360),
                    altitude=random.uniform(0, 3000)
                )
                db.add(gps)
                gps_count += 1
        db.commit()
        messages.append(f"✓ Created {gps_count} GPS tracking points")

        messages.append("=" * 50)
        messages.append("Database seeding completed successfully!")

        return {
            "status": "success",
            "message": "Database fully seeded with realistic fleet logistics data",
            "details": messages,
            "summary": {
                "organizations": len(orgs),
                "vehicles": len(vehicles),
                "drivers": len(drivers),
                "locations": len(locations),
                "routes": len(routes),
                "deliveries": NUM_DELIVERIES,
                "maintenance_records": maintenance_count,
                "fuel_logs": fuel_count,
                "incidents": incident_count,
                "gps_tracking": gps_count,
                "time_span": f"{HISTORY_MONTHS} months"
            }
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": str(e),
            "details": messages
        }

@router.delete("/clear")
def clear_database(db: Session = Depends(get_db)):
    """Clear all data from the database (use with caution!)"""
    try:
        db.query(GPSTracking).delete()
        db.query(Incident).delete()
        db.query(FuelLog).delete()
        db.query(MaintenanceRecord).delete()
        db.query(Delivery).delete()
        db.query(Route).delete()
        db.query(Location).delete()
        db.query(Driver).delete()
        db.query(Vehicle).delete()
        db.query(Organization).delete()
        db.commit()

        return {
            "status": "success",
            "message": "All data cleared from database"
        }
    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }
