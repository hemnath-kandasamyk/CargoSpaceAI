import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class ShipmentStatus:
    """Allowed status values. Kept as plain constants rather than a DB enum
    so new statuses can be added without a migration."""
    BOOKED = "booked"
    IN_TRANSIT = "in_transit"
    DELAYED = "delayed"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Shipment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "shipments"

    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    driver_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("drivers.id"), nullable=True)
    origin_warehouse_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=True)

    destination_address: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default=ShipmentStatus.BOOKED, nullable=False, index=True)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    declared_value: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    estimated_delivery: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    customer: Mapped["User"] = relationship(back_populates="shipments")
    driver: Mapped["Driver"] = relationship(back_populates="shipments")
    origin_warehouse: Mapped["Warehouse"] = relationship()
    tracking_history: Mapped[list["TrackingHistory"]] = relationship(
        back_populates="shipment", order_by="TrackingHistory.updated_at"
    )
    cargo_items: Mapped[list["CargoItem"]] = relationship(back_populates="shipment")
    payments: Mapped[list["Payment"]] = relationship(back_populates="shipment")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="shipment")
