from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import models, schemas
from app.database.config import get_db

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.get("/", response_model=List[schemas.Incident])
def get_incidents(
    skip: int = 0,
    limit: int = 100,
    driver_id: Optional[int] = None,
    incident_type: Optional[str] = None,
    severity: Optional[str] = None,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Incident)

    if driver_id:
        query = query.filter(models.Incident.driver_id == driver_id)
    if incident_type:
        query = query.filter(models.Incident.incident_type == incident_type)
    if severity:
        query = query.filter(models.Incident.severity == severity)
    if resolved is not None:
        query = query.filter(models.Incident.resolved == resolved)

    incidents = query.offset(skip).limit(limit).all()
    return incidents

@router.get("/{incident_id}", response_model=schemas.Incident)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.post("/", response_model=schemas.Incident)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
    db_incident = models.Incident(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.put("/{incident_id}", response_model=schemas.Incident)
def update_incident(incident_id: int, incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
    db_incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    for key, value in incident.dict().items():
        setattr(db_incident, key, value)

    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.delete("/{incident_id}")
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    db_incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    db.delete(db_incident)
    db.commit()
    return {"message": "Incident deleted successfully"}
