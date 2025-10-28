from sqlalchemy.orm import Session
from uuid import UUID
from .. import models
from ..schemas import vehicle as vehicle_schema

def get_all_vehicles(db: Session):
    return db.query(models.Vehicle).order_by(models.Vehicle.plate_number).all()

def create_vehicle(db: Session, vehicle: vehicle_schema.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def update_vehicle(db: Session, vehicle_id: UUID, vehicle_update: vehicle_schema.VehicleUpdate):
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.vehicle_id == vehicle_id).first()
    if not db_vehicle:
        return None
    for key, value in vehicle_update.dict(exclude_unset=True).items():
        setattr(db_vehicle, key, value)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def delete_vehicle(db: Session, vehicle_id: UUID):
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.vehicle_id == vehicle_id).first()
    if not db_vehicle:
        return False
    db.delete(db_vehicle)
    db.commit()
    return True