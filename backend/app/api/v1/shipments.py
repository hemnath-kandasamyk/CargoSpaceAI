import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.database.session import get_db
from app.models.shipment import Shipment
from app.models.user import User
from app.schemas.shipment import (
    ShipmentCreateRequest,
    ShipmentResponse,
    ShipmentTrackingResponse,
    TrackingHistoryEntry,
)
from app.services.shipment_service import (
    assert_owns_shipment_or_admin,
    create_shipment,
    get_shipment_or_404,
)

router = APIRouter(prefix="/shipments", tags=["Shipments"])


@router.post("", response_model=ShipmentResponse, status_code=201)
def create_new_shipment(
    payload: ShipmentCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("customer")),
):
    shipment = create_shipment(db, current_user.id, payload)
    return shipment


@router.get("/{shipment_id}/track", response_model=ShipmentTrackingResponse)
def track_shipment(
    shipment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    shipment = get_shipment_or_404(db, shipment_id)
    assert_owns_shipment_or_admin(shipment, current_user.id, current_user.role.name)

    history = [
        TrackingHistoryEntry(status=e.status, location=e.location, updated_at=e.updated_at)
        for e in shipment.tracking_history
    ]
    return ShipmentTrackingResponse(shipment=shipment, history=history)


@router.get("", response_model=list[ShipmentResponse])
def list_shipments(
    status: str | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Shipment)
    if current_user.role.name != "admin":
        query = query.filter_by(customer_id=current_user.id)
    if status:
        query = query.filter_by(status=status)

    return query.offset((page - 1) * page_size).limit(page_size).all()
