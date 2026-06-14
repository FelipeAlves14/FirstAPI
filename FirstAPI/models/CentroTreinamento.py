"""
Modelo de Centro de Treinamento.
"""

# pylint: disable=too-few-public-methods

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from FirstAPI.contrib.BaseModel import BaseModel

if TYPE_CHECKING:
    from FirstAPI.models.Atleta import AtletaModel


class CentroTreinamentoModel(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Representa um centro de treinamento.
    """

    __tablename__ = "centros_treinamento"

    pk_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    nome: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    endereco: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )

    proprietario: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    atleta: Mapped["AtletaModel"] = relationship(
        back_populates="centro_treinamento"
    )
