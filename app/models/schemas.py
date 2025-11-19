from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Organization Schemas
class OrganizationBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Vehicle Schemas
class VehicleBase(BaseModel):
    organization_id: int
    vin: str
    make: str
    model: str
    year: int
    license_plate: str
    vehicle_type: str
    capacity_kg: float
    current_mileage: float
    status: Optional[str] = "active"

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Driver Schemas
class DriverBase(BaseModel):
    organization_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    license_number: str
    license_expiry: datetime
    hire_date: datetime
    status: Optional[str] = "active"
    rating: Optional[float] = 5.0

class DriverCreate(DriverBase):
    pass

class Driver(DriverBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Location Schemas
class LocationBase(BaseModel):
    organization_id: int
    name: str
    type: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Route Schemas
class RouteBase(BaseModel):
    vehicle_id: int
    driver_id: int
    origin_location_id: int
    destination_location_id: int
    scheduled_departure: datetime
    scheduled_arrival: datetime
    distance_km: float
    status: Optional[str] = "scheduled"
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None

class RouteCreate(RouteBase):
    pass

class Route(RouteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Delivery Schemas
class DeliveryBase(BaseModel):
    route_id: int
    location_id: int
    tracking_number: str
    customer_name: str
    customer_email: str
    customer_phone: str
    package_count: int
    weight_kg: float
    scheduled_delivery: datetime
    status: Optional[str] = "pending"
    priority: Optional[str] = "standard"
    signature_required: Optional[bool] = False
    actual_delivery: Optional[datetime] = None
    delivery_notes: Optional[str] = None

class DeliveryCreate(DeliveryBase):
    pass

class Delivery(DeliveryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Maintenance Record Schemas
class MaintenanceRecordBase(BaseModel):
    vehicle_id: int
    maintenance_type: str
    description: str
    cost: float
    mileage_at_service: float
    service_date: datetime
    service_provider: str
    downtime_hours: float
    next_service_date: Optional[datetime] = None

class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass

class MaintenanceRecord(MaintenanceRecordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Fuel Log Schemas
class FuelLogBase(BaseModel):
    vehicle_id: int
    date: datetime
    location: str
    liters: float
    cost_per_liter: float
    total_cost: float
    mileage: float
    fuel_type: Optional[str] = "diesel"

class FuelLogCreate(FuelLogBase):
    pass

class FuelLog(FuelLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Incident Schemas
class IncidentBase(BaseModel):
    driver_id: int
    incident_type: str
    severity: str
    description: str
    date: datetime
    location: str
    resolved: Optional[bool] = False
    cost: Optional[float] = None
    resolution_notes: Optional[str] = None

class IncidentCreate(IncidentBase):
    pass

class Incident(IncidentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# GPS Tracking Schemas
class GPSTrackingBase(BaseModel):
    vehicle_id: int
    timestamp: datetime
    latitude: float
    longitude: float
    speed_kmh: float
    heading: float
    altitude: Optional[float] = None

class GPSTrackingCreate(GPSTrackingBase):
    pass

class GPSTracking(GPSTrackingBase):
    id: int

    class Config:
        from_attributes = True
