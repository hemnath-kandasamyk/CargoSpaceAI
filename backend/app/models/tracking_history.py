import uuid

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin


class TrackingHistory(Base, UUIDPrimaryKeyMixin):
    """
    Append-only log of shipment status changes.
    NEVER update or delete rows here — this is the ground-truth timeline
    shown to customers, and the training data for the delay-prediction model.
    """
    __tablename__ = "tracking_history"

    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    location: Mapped[str | None] = mapped_column(String(150), nullable=True)
    updated_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    shipment: Mapped["Shipment"] = relationship(back_populates="tracking_history")
