from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from enum import Enum

# Using Enums for strong validation against your business rules
class VehicleType(str, Enum):
    truck = "Truck"
    van = "Van"
    bike = "Bike"

class FuelType(str, Enum):
    EV = "EV"
    diesel = "Diesel"
    petrol = "Petrol"
    CNG = "CNG"

class VehicleStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"
    in_transit = "in-transit"

class VehicleBase(BaseModel):
    vehicle_type: VehicleType
    plate_number: str = Field(..., max_length=20)
    capacity_kg: float = Field(..., gt=0)
    fuel_type: FuelType
    driver_name: Optional[str] = None
    current_location: Optional[str] = None
    status: VehicleStatus = 'active'

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    pass

class VehiclePublic(VehicleBase):
    vehicle_id: UUID

    class Config:
        from_attributes = True