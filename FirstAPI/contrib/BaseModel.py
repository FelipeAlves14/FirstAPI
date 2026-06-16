"""Base SQLAlchemy model shared by ORM entities."""

# pylint: disable=invalid-name,import-error,too-few-public-methods

from uuid import uuid4

from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """Base ORM model with a UUID primary key."""

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, nullable=False)
