from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.config import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicles = relationship("Vehicle", back_populates="organization")
    drivers = relationship("Driver", back_populates="organization")
    locations = relationship("Location", back_populates="organization")

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    vin = Column(String, unique=True, index=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    license_plate = Column(String)
    vehicle_type = Column(String)  # truck, van, cargo, etc.
    capacity_kg = Column(Float)
    status = Column(String, default="active")  # active, maintenance, retired
    current_mileage = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="vehicles")
    routes = relationship("Route", back_populates="vehicle")
    maintenance_records = relationship("MaintenanceRecord", back_populates="vehicle")
    fuel_logs = relationship("FuelLog", back_populates="vehicle")
    gps_tracking = relationship("GPSTracking", back_populates="vehicle")

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    license_number = Column(String, unique=True)
    license_expiry = Column(DateTime)
    status = Column(String, default="active")  # active, inactive, on_leave
    hire_date = Column(DateTime)
    rating = Column(Float, default=5.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="drivers")
    routes = relationship("Route", back_populates="driver")
    incidents = relationship("Incident", back_populates="driver")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    name = Column(String)
    type = Column(String)  # warehouse, depot, customer, distribution_center
    address = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="locations")
    routes_origin = relationship("Route", foreign_keys="Route.origin_location_id", back_populates="origin_location")
    routes_destination = relationship("Route", foreign_keys="Route.destination_location_id", back_populates="destination_location")
    deliveries = relationship("Delivery", back_populates="location")

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    origin_location_id = Column(Integer, ForeignKey("locations.id"))
    destination_location_id = Column(Integer, ForeignKey("locations.id"))
    scheduled_departure = Column(DateTime)
    actual_departure = Column(DateTime, nullable=True)
    scheduled_arrival = Column(DateTime)
    actual_arrival = Column(DateTime, nullable=True)
    distance_km = Column(Float)
    status = Column(String, default="scheduled")  # scheduled, in_progress, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="routes")
    driver = relationship("Driver", back_populates="routes")
    origin_location = relationship("Location", foreign_keys=[origin_location_id], back_populates="routes_origin")
    destination_location = relationship("Location", foreign_keys=[destination_location_id], back_populates="routes_destination")
    deliveries = relationship("Delivery", back_populates="route")

class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    tracking_number = Column(String, unique=True, index=True)
    customer_name = Column(String)
    customer_email = Column(String)
    customer_phone = Column(String)
    package_count = Column(Integer)
    weight_kg = Column(Float)
    status = Column(String, default="pending")  # pending, in_transit, delivered, failed
    priority = Column(String, default="standard")  # standard, express, urgent
    scheduled_delivery = Column(DateTime)
    actual_delivery = Column(DateTime, nullable=True)
    delivery_notes = Column(Text, nullable=True)
    signature_required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    route = relationship("Route", back_populates="deliveries")
    location = relationship("Location", back_populates="deliveries")

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    maintenance_type = Column(String)  # routine, repair, inspection, emergency
    description = Column(Text)
    cost = Column(Numeric(10, 2))
    mileage_at_service = Column(Float)
    service_date = Column(DateTime)
    next_service_date = Column(DateTime, nullable=True)
    service_provider = Column(String)
    downtime_hours = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="maintenance_records")

class FuelLog(Base):
    __tablename__ = "fuel_logs"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    date = Column(DateTime)
    location = Column(String)
    liters = Column(Float)
    cost_per_liter = Column(Numeric(10, 2))
    total_cost = Column(Numeric(10, 2))
    mileage = Column(Float)
    fuel_type = Column(String, default="diesel")
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="fuel_logs")

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    incident_type = Column(String)  # accident, delay, damage, theft, violation
    severity = Column(String)  # minor, moderate, major, critical
    description = Column(Text)
    date = Column(DateTime)
    location = Column(String)
    cost = Column(Numeric(10, 2), nullable=True)
    resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    driver = relationship("Driver", back_populates="incidents")

class GPSTracking(Base):
    __tablename__ = "gps_tracking"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    timestamp = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    speed_kmh = Column(Float)
    heading = Column(Float)
    altitude = Column(Float, nullable=True)

    vehicle = relationship("Vehicle", back_populates="gps_tracking")
