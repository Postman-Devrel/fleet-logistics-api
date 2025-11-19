import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from datetime import datetime, timedelta
import random
from app.database.config import SessionLocal, engine
from app.models.models import (
    Base, Organization, Vehicle, Driver, Location, Route,
    Delivery, MaintenanceRecord, FuelLog, Incident, GPSTracking
)

fake = Faker()
Faker.seed(42)
random.seed(42)

# Configuration
NUM_ORGANIZATIONS = 3
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

# Location types
LOCATION_TYPES = ["warehouse", "depot", "customer", "distribution_center"]

# US States for locations
US_STATES = ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI"]

def create_database():
    Base.metadata.create_all(bind=engine)

def generate_vin():
    """Generate a fake but realistic VIN"""
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    return ''.join(random.choice(chars) for _ in range(17))

def generate_tracking_number():
    """Generate a fake tracking number"""
    return f"TRK{random.randint(100000000, 999999999)}"

def seed_organizations(db):
    print("Seeding organizations...")
    organizations = []
    company_names = [
        "Swift Logistics Inc",
        "National Transport Co",
        "Premier Freight Services"
    ]

    for name in company_names:
        org = Organization(
            name=name,
            email=fake.company_email(),
            phone=fake.phone_number(),
            address=fake.address().replace('\n', ', '),
            created_at=datetime.utcnow() - timedelta(days=random.randint(365, 1825))
        )
        organizations.append(org)
        db.add(org)

    db.commit()
    return organizations

def seed_vehicles(db, organizations):
    print(f"Seeding {NUM_VEHICLES} vehicles...")
    vehicles = []
    base_date = datetime.utcnow() - timedelta(days=HISTORY_MONTHS * 30)

    for i in range(NUM_VEHICLES):
        make = random.choice(VEHICLE_MAKES)
        model = random.choice(VEHICLE_MODELS[make])
        year = random.randint(2015, 2024)
        org = random.choice(organizations)

        vehicle = Vehicle(
            organization_id=org.id,
            vin=generate_vin(),
            make=make,
            model=model,
            year=year,
            license_plate=f"{fake.random_letter().upper()}{fake.random_letter().upper()}{random.randint(1000, 9999)}",
            vehicle_type=random.choice(VEHICLE_TYPES),
            capacity_kg=random.choice([1000, 2000, 5000, 10000, 20000]),
            status=random.choices(["active", "maintenance", "retired"], weights=[0.85, 0.13, 0.02])[0],
            current_mileage=random.uniform(10000, 500000),
            created_at=base_date + timedelta(days=random.randint(0, 60))
        )
        vehicles.append(vehicle)
        db.add(vehicle)

    db.commit()
    return vehicles

def seed_drivers(db, organizations):
    print(f"Seeding {NUM_DRIVERS} drivers...")
    drivers = []
    base_date = datetime.utcnow() - timedelta(days=HISTORY_MONTHS * 30)

    for i in range(NUM_DRIVERS):
        org = random.choice(organizations)
        hire_date = base_date + timedelta(days=random.randint(0, HISTORY_MONTHS * 30))

        driver = Driver(
            organization_id=org.id,
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
    return drivers

def seed_locations(db, organizations):
    print(f"Seeding {NUM_LOCATIONS} locations...")
    locations = []

    for i in range(NUM_LOCATIONS):
        org = random.choice(organizations)
        lat = random.uniform(25.0, 48.0)
        lon = random.uniform(-125.0, -65.0)

        location = Location(
            organization_id=org.id,
            name=f"{fake.company()} - {fake.city()}",
            type=random.choice(LOCATION_TYPES),
            address=fake.street_address(),
            city=fake.city(),
            state=random.choice(US_STATES),
            postal_code=fake.zipcode(),
            country="USA",
            latitude=lat,
            longitude=lon,
            created_at=datetime.utcnow() - timedelta(days=random.randint(30, HISTORY_MONTHS * 30))
        )
        locations.append(location)
        db.add(location)

    db.commit()
    return locations

def seed_routes(db, vehicles, drivers, locations):
    print(f"Seeding {NUM_ROUTES} routes...")
    routes = []
    base_date = datetime.utcnow() - timedelta(days=HISTORY_MONTHS * 30)

    for i in range(NUM_ROUTES):
        vehicle = random.choice(vehicles)
        driver = random.choice(drivers)
        origin = random.choice(locations)
        destination = random.choice([loc for loc in locations if loc.id != origin.id])

        scheduled_departure = base_date + timedelta(days=random.randint(0, HISTORY_MONTHS * 30), hours=random.randint(0, 23))
        distance_km = random.uniform(50, 2000)
        duration_hours = distance_km / random.uniform(60, 80)
        scheduled_arrival = scheduled_departure + timedelta(hours=duration_hours)

        status = random.choices(
            ["scheduled", "in_progress", "completed", "cancelled"],
            weights=[0.1, 0.05, 0.8, 0.05]
        )[0]

        actual_departure = None
        actual_arrival = None
        if status in ["in_progress", "completed"]:
            actual_departure = scheduled_departure + timedelta(minutes=random.randint(-30, 60))
            if status == "completed":
                actual_arrival = scheduled_arrival + timedelta(minutes=random.randint(-60, 120))

        route = Route(
            vehicle_id=vehicle.id,
            driver_id=driver.id,
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
    return routes

def seed_deliveries(db, routes, locations):
    print(f"Seeding {NUM_DELIVERIES} deliveries...")

    # Distribute deliveries across routes
    for i in range(NUM_DELIVERIES):
        route = random.choice(routes)
        location = random.choice(locations)

        scheduled_delivery = route.scheduled_arrival + timedelta(hours=random.randint(0, 48))

        status_weights = [0.05, 0.1, 0.83, 0.02] if route.status == "completed" else [0.7, 0.2, 0.08, 0.02]
        status = random.choices(
            ["pending", "in_transit", "delivered", "failed"],
            weights=status_weights
        )[0]

        actual_delivery = None
        if status == "delivered":
            actual_delivery = scheduled_delivery + timedelta(hours=random.randint(-12, 24))

        delivery = Delivery(
            route_id=route.id,
            location_id=location.id,
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

def seed_maintenance_records(db, vehicles):
    print("Seeding maintenance records...")
    base_date = datetime.utcnow() - timedelta(days=HISTORY_MONTHS * 30)

    for vehicle in vehicles:
        # Each vehicle has 2-6 maintenance records over 6 months
        num_records = random.randint(2, 6)
        for i in range(num_records):
            service_date = base_date + timedelta(days=random.randint(0, HISTORY_MONTHS * 30))

            maintenance_type = random.choice(["routine", "repair", "inspection", "emergency"])
            descriptions = {
                "routine": ["Oil change and filter replacement", "Tire rotation", "Brake inspection"],
                "repair": ["Engine repair", "Transmission service", "Suspension repair"],
                "inspection": ["Annual DOT inspection", "Safety inspection", "Emissions test"],
                "emergency": ["Roadside breakdown repair", "Accident damage repair", "Tow service"]
            }

            maintenance = MaintenanceRecord(
                vehicle_id=vehicle.id,
                maintenance_type=maintenance_type,
                description=random.choice(descriptions[maintenance_type]),
                cost=random.uniform(100, 5000),
                mileage_at_service=vehicle.current_mileage - random.uniform(0, 50000),
                service_date=service_date,
                next_service_date=service_date + timedelta(days=random.randint(30, 180)) if maintenance_type == "routine" else None,
                service_provider=fake.company(),
                downtime_hours=random.uniform(1, 48) if maintenance_type in ["repair", "emergency"] else random.uniform(0.5, 4),
                created_at=service_date
            )
            db.add(maintenance)

    db.commit()

def seed_fuel_logs(db, vehicles):
    print("Seeding fuel logs...")
    base_date = datetime.utcnow() - timedelta(days=HISTORY_MONTHS * 30)

    for vehicle in vehicles:
        # Each vehicle refuels 20-40 times over 6 months
        num_logs = random.randint(20, 40)
        current_mileage = vehicle.current_mileage - random.uniform(10000, 50000)

        for i in range(num_logs):
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
                mileage=current_mileage,
                fuel_type=random.choices(["diesel", "gasoline", "electric"], weights=[0.7, 0.25, 0.05])[0],
                created_at=fuel_date
            )
            db.add(fuel_log)
            current_mileage += random.uniform(200, 800)

    db.commit()

def seed_incidents(db, drivers):
    print("Seeding incidents...")
    base_date = datetime.utcnow() - timedelta(days=HISTORY_MONTHS * 30)

    # Not all drivers have incidents
    drivers_with_incidents = random.sample(drivers, k=int(len(drivers) * 0.3))

    for driver in drivers_with_incidents:
        num_incidents = random.randint(1, 3)

        for i in range(num_incidents):
            incident_date = base_date + timedelta(days=random.randint(0, HISTORY_MONTHS * 30))
            incident_type = random.choice(["accident", "delay", "damage", "theft", "violation"])

            severity_weights = {
                "accident": [0.5, 0.3, 0.15, 0.05],
                "delay": [0.7, 0.25, 0.05, 0.0],
                "damage": [0.4, 0.4, 0.15, 0.05],
                "theft": [0.2, 0.3, 0.3, 0.2],
                "violation": [0.6, 0.3, 0.08, 0.02]
            }

            severity = random.choices(
                ["minor", "moderate", "major", "critical"],
                weights=severity_weights[incident_type]
            )[0]

            resolved = incident_date < datetime.utcnow() - timedelta(days=7)

            incident = Incident(
                driver_id=driver.id,
                incident_type=incident_type,
                severity=severity,
                description=fake.sentence(),
                date=incident_date,
                location=f"{fake.street_address()}, {fake.city()}, {random.choice(US_STATES)}",
                cost=random.uniform(100, 10000) if incident_type in ["accident", "damage", "theft"] else None,
                resolved=resolved,
                resolution_notes=fake.sentence() if resolved else None,
                created_at=incident_date
            )
            db.add(incident)

    db.commit()

def seed_gps_tracking(db, vehicles):
    print("Seeding GPS tracking data...")
    base_date = datetime.utcnow() - timedelta(days=HISTORY_MONTHS * 30)

    # Generate GPS data for active vehicles over the last 30 days
    recent_date = datetime.utcnow() - timedelta(days=30)

    for vehicle in random.sample(vehicles, k=min(30, len(vehicles))):
        # Generate 50-200 GPS points per vehicle
        num_points = random.randint(50, 200)

        # Start at a random location
        lat = random.uniform(25.0, 48.0)
        lon = random.uniform(-125.0, -65.0)

        for i in range(num_points):
            timestamp = recent_date + timedelta(minutes=random.uniform(0, 30 * 24 * 60))

            # Simulate movement
            lat += random.uniform(-0.1, 0.1)
            lon += random.uniform(-0.1, 0.1)

            # Keep within US bounds
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

    db.commit()

def main():
    print("Starting database seeding...")
    print("=" * 60)

    # Create database tables
    create_database()

    # Create database session
    db = SessionLocal()

    try:
        # Seed data in order
        organizations = seed_organizations(db)
        vehicles = seed_vehicles(db, organizations)
        drivers = seed_drivers(db, organizations)
        locations = seed_locations(db, organizations)
        routes = seed_routes(db, vehicles, drivers, locations)
        seed_deliveries(db, routes, locations)
        seed_maintenance_records(db, vehicles)
        seed_fuel_logs(db, vehicles)
        seed_incidents(db, drivers)
        seed_gps_tracking(db, vehicles)

        print("=" * 60)
        print("Database seeding completed successfully!")
        print(f"Organizations: {len(organizations)}")
        print(f"Vehicles: {len(vehicles)}")
        print(f"Drivers: {len(drivers)}")
        print(f"Locations: {len(locations)}")
        print(f"Routes: {len(routes)}")
        print(f"Deliveries: {NUM_DELIVERIES}")
        print("Plus maintenance records, fuel logs, incidents, and GPS tracking data")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
