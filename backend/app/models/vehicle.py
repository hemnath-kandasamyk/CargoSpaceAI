from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin


class Vehicle(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "vehicles"

    plate_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String(30), nullable=False)  # van, truck, bike
    capacity_kg: Mapped[float] = mapped_column(Float, nullable=False)

    drivers: Mapped[list["Driver"]] = relationship(back_populates="vehicle")
