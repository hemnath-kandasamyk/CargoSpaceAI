from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin


class Warehouse(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "warehouses"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(150), nullable=False)
    capacity_units: Mapped[int] = mapped_column(Integer, nullable=False)
    current_load_units: Mapped[int] = mapped_column(Integer, default=0)

    cargo_items: Mapped[list["CargoItem"]] = relationship(back_populates="warehouse")
