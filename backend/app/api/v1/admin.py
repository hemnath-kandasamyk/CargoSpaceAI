from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.database.session import get_db
from app.models.shipment import Shipment, ShipmentStatus
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/reports/analytics")
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    total_shipments = db.query(func.count(Shipment.id)).scalar()
    delivered = db.query(func.count(Shipment.id)).filter(Shipment.status == ShipmentStatus.DELIVERED).scalar()
    delayed = db.query(func.count(Shipment.id)).filter(Shipment.status == ShipmentStatus.DELAYED).scalar()

    on_time_rate = (delivered / total_shipments) if total_shipments else 0.0

    return {
        "total_shipments": total_shipments,
        "delivered": delivered,
        "delayed": delayed,
        "on_time_rate": round(on_time_rate, 3),
    }


@router.get("/users")
def list_users(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    users = db.query(User).offset((page - 1) * page_size).limit(page_size).all()
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role.name} for u in users]
