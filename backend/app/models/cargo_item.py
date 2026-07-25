import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin


class CargoItem(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "cargo_items"

    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False)
    warehouse_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    qr_code: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(30), default="pending")  # pending, in_warehouse, dispatched

    shipment: Mapped["Shipment"] = relationship(back_populates="cargo_items")
    warehouse: Mapped["Warehouse"] = relationship(back_populates="cargo_items")
