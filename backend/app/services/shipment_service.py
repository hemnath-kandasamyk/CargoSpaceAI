"""
Shipment lifecycle logic.
Key rule: shipment.status is a denormalized "current state" convenience
field, but the source of truth is the append-only TrackingHistory log.
Every status change must go through `append_tracking_event` so both
stay in sync — never update shipment.status without also logging history.
"""
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.shipment import Shipment, ShipmentStatus
from app.models.tracking_history import TrackingHistory
from app.schemas.shipment import ShipmentCreateRequest
from app.utils import error_codes


def create_shipment(db: Session, customer_id: uuid.UUID, payload: ShipmentCreateRequest) -> Shipment:
    shipment = Shipment(
        customer_id=customer_id,
        destination_address=payload.destination_address,
        weight_kg=payload.weight_kg,
        declared_value=payload.declared_value,
        origin_warehouse_id=payload.origin_warehouse_id,
        status=ShipmentStatus.BOOKED,
    )
    db.add(shipment)
    db.flush()  # get shipment.id before commit

    append_tracking_event(db, shipment.id, ShipmentStatus.BOOKED, location=None, commit=False)

    db.commit()
    db.refresh(shipment)
    return shipment


def append_tracking_event(
    db: Session, shipment_id: uuid.UUID, new_status: str, location: str | None, commit: bool = True
) -> TrackingHistory:
    event = TrackingHistory(shipment_id=shipment_id, status=new_status, location=location)
    db.add(event)

    shipment = db.get(Shipment, shipment_id)
    if shipment:
        shipment.status = new_status

    if commit:
        db.commit()
        db.refresh(event)
    return event


def get_shipment_or_404(db: Session, shipment_id: uuid.UUID) -> Shipment:
    shipment = db.get(Shipment, shipment_id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": error_codes.RESOURCE_NOT_FOUND, "message": "Shipment not found."},
        )
    return shipment


def assert_owns_shipment_or_admin(shipment: Shipment, user_id: uuid.UUID, role: str) -> None:
    if role == "admin":
        return
    if shipment.customer_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error_code": error_codes.PERMISSION_DENIED, "message": "Not your shipment."},
        )
