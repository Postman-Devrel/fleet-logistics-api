from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import models, schemas
from app.database.config import get_db

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

@router.get("/", response_model=List[schemas.MaintenanceRecord])
def get_maintenance_records(
    skip: int = 0,
    limit: int = 100,
    vehicle_id: Optional[int] = None,
    maintenance_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.MaintenanceRecord)

    if vehicle_id:
        query = query.filter(models.MaintenanceRecord.vehicle_id == vehicle_id)
    if maintenance_type:
        query = query.filter(models.MaintenanceRecord.maintenance_type == maintenance_type)

    records = query.offset(skip).limit(limit).all()
    return records

@router.get("/{record_id}", response_model=schemas.MaintenanceRecord)
def get_maintenance_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(models.MaintenanceRecord).filter(models.MaintenanceRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return record

@router.post("/", response_model=schemas.MaintenanceRecord)
def create_maintenance_record(record: schemas.MaintenanceRecordCreate, db: Session = Depends(get_db)):
    db_record = models.MaintenanceRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.put("/{record_id}", response_model=schemas.MaintenanceRecord)
def update_maintenance_record(record_id: int, record: schemas.MaintenanceRecordCreate, db: Session = Depends(get_db)):
    db_record = db.query(models.MaintenanceRecord).filter(models.MaintenanceRecord.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    for key, value in record.dict().items():
        setattr(db_record, key, value)

    db.commit()
    db.refresh(db_record)
    return db_record

@router.delete("/{record_id}")
def delete_maintenance_record(record_id: int, db: Session = Depends(get_db)):
    db_record = db.query(models.MaintenanceRecord).filter(models.MaintenanceRecord.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    db.delete(db_record)
    db.commit()
    return {"message": "Maintenance record deleted successfully"}
