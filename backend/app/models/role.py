from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin


class Role(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    # one of: customer, driver, warehouse_staff, admin

    users: Mapped[list["User"]] = relationship(back_populates="role")
