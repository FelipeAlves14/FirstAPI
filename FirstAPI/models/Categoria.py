from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from FirstAPI.contrib.BaseModel import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FirstAPI.models.Atleta import AtletaModel


class CategoriaModel(BaseModel):
    __tablename__ = "categorias"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key = True)
    nome: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    atleta: Mapped["AtletaModel"] = relationship(back_populates="categoria")