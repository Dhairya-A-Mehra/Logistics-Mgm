from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

# The request body for the shipment creation endpoint.
# The only thing the admin needs to provide is the ID of the order to ship.
class ShipmentCreateSchema(BaseModel):
    order_id: UUID = Field(..., description="The ID of the existing order to create a shipment for.")

# The public representation of a created shipment.
class ShipmentPublicSchema(BaseModel):
    shipment_id: UUID
    order_id: UUID
    origin_warehouse_id: UUID
    vehicle_id: UUID
    status: str
    shipped_at: datetime

    class Config:
        from_attributes = True