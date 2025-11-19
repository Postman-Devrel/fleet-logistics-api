from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import models, schemas
from app.database.config import get_db

router = APIRouter(prefix="/routes", tags=["routes"])

@router.get("/", response_model=List[schemas.Route])
def get_routes(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    vehicle_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Route)

    if status:
        query = query.filter(models.Route.status == status)
    if vehicle_id:
        query = query.filter(models.Route.vehicle_id == vehicle_id)
    if driver_id:
        query = query.filter(models.Route.driver_id == driver_id)

    routes = query.offset(skip).limit(limit).all()
    return routes

@router.get("/{route_id}", response_model=schemas.Route)
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.post("/", response_model=schemas.Route)
def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    db_route = models.Route(**route.dict())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

@router.put("/{route_id}", response_model=schemas.Route)
def update_route(route_id: int, route: schemas.RouteCreate, db: Session = Depends(get_db)):
    db_route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")

    for key, value in route.dict().items():
        setattr(db_route, key, value)

    db.commit()
    db.refresh(db_route)
    return db_route

@router.delete("/{route_id}")
def delete_route(route_id: int, db: Session = Depends(get_db)):
    db_route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")

    db.delete(db_route)
    db.commit()
    return {"message": "Route deleted successfully"}
