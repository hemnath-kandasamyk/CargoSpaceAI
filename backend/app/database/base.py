"""
Declarative base shared by every SQLAlchemy model.
Importing all models here (at the bottom) ensures Alembic's autogenerate
can see the full metadata when it inspects Base.metadata.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
