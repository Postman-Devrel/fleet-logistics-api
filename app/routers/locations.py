from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import models, schemas
from app.database.config import get_db

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("/", response_model=List[schemas.Location])
def get_locations(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    organization_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Location)

    if type:
        query = query.filter(models.Location.type == type)
    if city:
        query = query.filter(models.Location.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(models.Location.state == state)
    if organization_id:
        query = query.filter(models.Location.organization_id == organization_id)

    locations = query.offset(skip).limit(limit).all()
    return locations

@router.get("/{location_id}", response_model=schemas.Location)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.post("/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    db_location = models.Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.put("/{location_id}", response_model=schemas.Location)
def update_location(location_id: int, location: schemas.LocationCreate, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")

    for key, value in location.dict().items():
        setattr(db_location, key, value)

    db.commit()
    db.refresh(db_location)
    return db_location

@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")

    db.delete(db_location)
    db.commit()
    return {"message": "Location deleted successfully"}
