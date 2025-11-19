from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models import models, schemas
from app.database.config import get_db

router = APIRouter(prefix="/deliveries", tags=["deliveries"])

@router.get("/", response_model=List[schemas.Delivery])
def get_deliveries(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    route_id: Optional[int] = None,
    tracking_number: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Delivery)

    if status:
        query = query.filter(models.Delivery.status == status)
    if priority:
        query = query.filter(models.Delivery.priority == priority)
    if route_id:
        query = query.filter(models.Delivery.route_id == route_id)
    if tracking_number:
        query = query.filter(models.Delivery.tracking_number.ilike(f"%{tracking_number}%"))

    deliveries = query.offset(skip).limit(limit).all()
    return deliveries

@router.get("/{delivery_id}", response_model=schemas.Delivery)
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery

@router.get("/tracking/{tracking_number}", response_model=schemas.Delivery)
def get_delivery_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    delivery = db.query(models.Delivery).filter(models.Delivery.tracking_number == tracking_number).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery

@router.post("/", response_model=schemas.Delivery)
def create_delivery(delivery: schemas.DeliveryCreate, db: Session = Depends(get_db)):
    db_delivery = models.Delivery(**delivery.dict())
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@router.put("/{delivery_id}", response_model=schemas.Delivery)
def update_delivery(delivery_id: int, delivery: schemas.DeliveryCreate, db: Session = Depends(get_db)):
    db_delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    for key, value in delivery.dict().items():
        setattr(db_delivery, key, value)

    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@router.delete("/{delivery_id}")
def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    db_delivery = db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    db.delete(db_delivery)
    db.commit()
    return {"message": "Delivery deleted successfully"}
