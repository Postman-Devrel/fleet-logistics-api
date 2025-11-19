from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import models, schemas
from app.database.config import get_db

router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.get("/", response_model=List[schemas.Driver])
def get_drivers(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    organization_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Driver)

    if status:
        query = query.filter(models.Driver.status == status)
    if organization_id:
        query = query.filter(models.Driver.organization_id == organization_id)

    drivers = query.offset(skip).limit(limit).all()
    return drivers

@router.get("/{driver_id}", response_model=schemas.Driver)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@router.post("/", response_model=schemas.Driver)
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    db_driver = models.Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver

@router.put("/{driver_id}", response_model=schemas.Driver)
def update_driver(driver_id: int, driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    db_driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    for key, value in driver.dict().items():
        setattr(db_driver, key, value)

    db.commit()
    db.refresh(db_driver)
    return db_driver

@router.delete("/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    db_driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    db.delete(db_driver)
    db.commit()
    return {"message": "Driver deleted successfully"}
