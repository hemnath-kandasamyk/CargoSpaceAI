import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin


class Driver(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "drivers"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    vehicle_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=True)
    license_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    vehicle: Mapped["Vehicle"] = relationship(back_populates="drivers")
    shipments: Mapped[list["Shipment"]] = relationship(back_populates="driver")
