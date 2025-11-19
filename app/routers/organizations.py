from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import models, schemas
from app.database.config import get_db

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.get("/", response_model=List[schemas.Organization])
def get_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    organizations = db.query(models.Organization).offset(skip).limit(limit).all()
    return organizations

@router.get("/{organization_id}", response_model=schemas.Organization)
def get_organization(organization_id: int, db: Session = Depends(get_db)):
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.post("/", response_model=schemas.Organization)
def create_organization(organization: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    db_organization = models.Organization(**organization.dict())
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization

@router.put("/{organization_id}", response_model=schemas.Organization)
def update_organization(organization_id: int, organization: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    db_organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not db_organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    for key, value in organization.dict().items():
        setattr(db_organization, key, value)

    db.commit()
    db.refresh(db_organization)
    return db_organization

@router.delete("/{organization_id}")
def delete_organization(organization_id: int, db: Session = Depends(get_db)):
    db_organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not db_organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    db.delete(db_organization)
    db.commit()
    return {"message": "Organization deleted successfully"}
