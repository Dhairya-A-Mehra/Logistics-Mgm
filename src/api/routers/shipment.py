from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from ... import security, database
from ...schemas import shipment as shipment_schema
from ...services import shipment_service
from ...models import Customer

router = APIRouter()

@router.post(
    "/",
    response_model=shipment_schema.ShipmentPublicSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new shipment for an order (Admin Only)",
    description="Creates a shipment by assigning a warehouse and vehicle to a pending order."
)
def create_shipment(
    shipment_data: shipment_schema.ShipmentCreateSchema,
    db: Session = Depends(database.get_db),
    # This endpoint is protected and can only be accessed by an admin
    current_user: Customer = Depends(security.get_admin_user)
):
    try:
        new_shipment = shipment_service.create_shipment_for_order(
            db=db,
            order_id=shipment_data.order_id
        )
        return new_shipment
    except HTTPException as e:
        # Re-raise known HTTP exceptions from the service layer
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )