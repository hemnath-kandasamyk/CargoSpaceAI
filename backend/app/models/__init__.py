"""
Import every model here so Base.metadata is fully populated —
this is what Alembic's `--autogenerate` inspects to detect schema changes,
and what SQLAlchemy needs to resolve string-based relationship() references.
"""
from app.models.role import Role
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.warehouse import Warehouse
from app.models.shipment import Shipment
from app.models.tracking_history import TrackingHistory
from app.models.cargo_item import CargoItem
from app.models.payment import Payment
from app.models.notification import Notification
from app.models.audit_log import AuditLog

__all__ = [
    "Role",
    "User",
    "Vehicle",
    "Driver",
    "Warehouse",
    "Shipment",
    "TrackingHistory",
    "CargoItem",
    "Payment",
    "Notification",
    "AuditLog",
]
