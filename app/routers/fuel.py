from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import models, schemas
from app.database.config import get_db

router = APIRouter(prefix="/fuel", tags=["fuel"])

@router.get("/", response_model=List[schemas.FuelLog])
def get_fuel_logs(
    skip: int = 0,
    limit: int = 100,
    vehicle_id: Optional[int] = None,
    fuel_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.FuelLog)

    if vehicle_id:
        query = query.filter(models.FuelLog.vehicle_id == vehicle_id)
    if fuel_type:
        query = query.filter(models.FuelLog.fuel_type == fuel_type)

    logs = query.offset(skip).limit(limit).all()
    return logs

@router.get("/{log_id}", response_model=schemas.FuelLog)
def get_fuel_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(models.FuelLog).filter(models.FuelLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Fuel log not found")
    return log

@router.post("/", response_model=schemas.FuelLog)
def create_fuel_log(log: schemas.FuelLogCreate, db: Session = Depends(get_db)):
    db_log = models.FuelLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.put("/{log_id}", response_model=schemas.FuelLog)
def update_fuel_log(log_id: int, log: schemas.FuelLogCreate, db: Session = Depends(get_db)):
    db_log = db.query(models.FuelLog).filter(models.FuelLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Fuel log not found")

    for key, value in log.dict().items():
        setattr(db_log, key, value)

    db.commit()
    db.refresh(db_log)
    return db_log

@router.delete("/{log_id}")
def delete_fuel_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(models.FuelLog).filter(models.FuelLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Fuel log not found")

    db.delete(db_log)
    db.commit()
    return {"message": "Fuel log deleted successfully"}
