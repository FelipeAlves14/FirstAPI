"""Modelo da entidade Categoria."""

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from FirstAPI.contrib.BaseModel import BaseModel

if TYPE_CHECKING:
    from FirstAPI.models.Atleta import AtletaModel


# pylint: disable=too-few-public-methods
class CategoriaModel(BaseModel):
    """Representa uma categoria de atletas."""

    __tablename__ = "categorias"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
    )
    atleta: Mapped["AtletaModel"] = relationship(
        back_populates="categoria",
    )
