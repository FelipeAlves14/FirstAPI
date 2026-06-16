"""
Modelo da entidade Atleta.
"""

# pylint: disable=invalid-name,import-error

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from FirstAPI.contrib.BaseModel import BaseModel

if TYPE_CHECKING:
    from FirstAPI.models.Categoria import CategoriaModel
    from FirstAPI.models.CentroTreinamento import CentroTreinamentoModel


class AtletaModel(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Modelo responsÃ¡vel por representar um atleta.
    """

    __tablename__ = "atletas"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    categoria: Mapped["CategoriaModel"] = relationship(
        back_populates="atleta",
        lazy="selectin",
    )

    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.pk_id")
    )

    centro_treinamento: Mapped["CentroTreinamentoModel"] = relationship(
        back_populates="atleta",
        lazy="selectin",
    )

    centro_treinamento_id: Mapped[int] = mapped_column(
        ForeignKey("centros_treinamento.pk_id")
    )
