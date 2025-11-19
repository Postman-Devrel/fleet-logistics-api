from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models import models, schemas
from app.database.config import get_db

router = APIRouter(prefix="/gps", tags=["gps-tracking"])

@router.get("/", response_model=List[schemas.GPSTracking])
def get_gps_tracking(
    skip: int = 0,
    limit: int = 100,
    vehicle_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.GPSTracking)

    if vehicle_id:
        query = query.filter(models.GPSTracking.vehicle_id == vehicle_id)

    tracking = query.order_by(models.GPSTracking.timestamp.desc()).offset(skip).limit(limit).all()
    return tracking

@router.get("/vehicle/{vehicle_id}/latest", response_model=schemas.GPSTracking)
def get_latest_gps_for_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    tracking = db.query(models.GPSTracking).filter(
        models.GPSTracking.vehicle_id == vehicle_id
    ).order_by(models.GPSTracking.timestamp.desc()).first()

    if not tracking:
        raise HTTPException(status_code=404, detail="No GPS tracking data found for this vehicle")
    return tracking

@router.get("/{tracking_id}", response_model=schemas.GPSTracking)
def get_gps_tracking_by_id(tracking_id: int, db: Session = Depends(get_db)):
    tracking = db.query(models.GPSTracking).filter(models.GPSTracking.id == tracking_id).first()
    if not tracking:
        raise HTTPException(status_code=404, detail="GPS tracking record not found")
    return tracking

@router.post("/", response_model=schemas.GPSTracking)
def create_gps_tracking(tracking: schemas.GPSTrackingCreate, db: Session = Depends(get_db)):
    db_tracking = models.GPSTracking(**tracking.dict())
    db.add(db_tracking)
    db.commit()
    db.refresh(db_tracking)
    return db_tracking

@router.delete("/{tracking_id}")
def delete_gps_tracking(tracking_id: int, db: Session = Depends(get_db)):
    db_tracking = db.query(models.GPSTracking).filter(models.GPSTracking.id == tracking_id).first()
    if not db_tracking:
        raise HTTPException(status_code=404, detail="GPS tracking record not found")

    db.delete(db_tracking)
    db.commit()
    return {"message": "GPS tracking record deleted successfully"}
