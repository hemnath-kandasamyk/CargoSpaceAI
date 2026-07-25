import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.database.session import get_db
from app.models.driver import Driver
from app.models.shipment import Shipment
from app.models.user import User
from app.schemas.driver import AssignedDeliveryResponse, DeliveryStatusUpdateRequest
from app.schemas.shipment import ShipmentResponse
from app.services.shipment_service import append_tracking_event, get_shipment_or_404

router = APIRouter(prefix="/driver", tags=["Driver"])


@router.get("/deliveries", response_model=list[AssignedDeliveryResponse])
def get_assigned_deliveries(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("driver")),
):
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()
    if driver is None:
        return []
    return db.query(Shipment).filter(Shipment.driver_id == driver.id).all()


@router.patch("/deliveries/{shipment_id}", response_model=ShipmentResponse)
def update_delivery_status(
    shipment_id: uuid.UUID,
    payload: DeliveryStatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("driver")),
):
    shipment = get_shipment_or_404(db, shipment_id)
    # Appends to tracking_history AND updates shipment.status together —
    # see services/shipment_service.py for why these must stay in sync.
    append_tracking_event(db, shipment.id, payload.status, location=None)
    db.refresh(shipment)
    return shipment
