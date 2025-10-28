from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from enum import Enum
# --- EXISTING SCHEMAS (Unchanged) ---
class ShipmentCreateSchema(BaseModel):
    order_id: UUID = Field(..., description="The ID of the existing order to create a shipment for.")

class ShipmentPublicSchema(BaseModel):
    shipment_id: UUID
    order_id: UUID
    origin_warehouse_id: UUID
    vehicle_id: UUID
    status: str
    shipped_at: datetime
    class Config:
        from_attributes = True

# --- NEW SCHEMAS FOR THE "MY DELIVERIES" ENDPOINT ---

# A nested schema to represent basic customer info
class CustomerInfoForShipment(BaseModel):
    name: str
    class Config:
        from_attributes = True

# A nested schema to represent the destination address
class DestinationForShipment(BaseModel):
    address: str
    city: str
    class Config:
        from_attributes = True

# A nested schema to represent the order linked to the shipment
class OrderInfoForShipment(BaseModel):
    customer: CustomerInfoForShipment
    destination: DestinationForShipment
    class Config:
        from_attributes = True

# The main response schema for a single delivery item
class DriverShipmentDetailSchema(BaseModel):
    shipment_id: UUID
    status: str
    current_eta: Optional[datetime] = None
    order: OrderInfoForShipment
    class Config:
        from_attributes = True

class ShipmentStatusEnum(str, Enum):
    delivered = "delivered"
    # In the future, you could add other statuses like 'delivery_failed'

# This is the Pydantic model for the request body of our new PATCH endpoint.
class ShipmentStatusUpdate(BaseModel):
    status: ShipmentStatusEnum