"""Base schemas shared by the API."""

# pylint: disable=invalid-name

from datetime import datetime
from typing import Annotated

from pydantic import UUID4, BaseModel, Field


class BaseSchema(BaseModel):
    """Base schema with common Pydantic settings."""

    # pylint: disable=too-few-public-methods
    class Config:
        """Pydantic model configuration."""

        extra = "forbid"
        from_attributes = True
        arbitrary_types_allowed = True


class OutMixin(BaseSchema):
    """Common output fields returned by API schemas."""

    id: Annotated[UUID4, Field(description="ID")]
    created_at: Annotated[datetime, Field(description="Data de criação")]
