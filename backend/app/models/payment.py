import uuid

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin


class Payment(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "payments"

    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, paid, failed

    shipment: Mapped["Shipment"] = relationship(back_populates="payments")
