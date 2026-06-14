"""
Schemas relacionados às categorias.
"""

from typing import Annotated

from pydantic import UUID4, Field

from FirstAPI.contrib.BaseSchema import BaseSchema


class CategoriaIn(BaseSchema):
    """Schema para criação de categorias."""

    nome: Annotated[
        str,
        Field(
            description="Nome da categoria",
            examples=["Futebol"],
            max_length=10,
        ),
    ]


class CategoriaOut(CategoriaIn):
    """Schema de retorno de categorias."""

    id: Annotated[
        UUID4,
        Field(description="ID"),
    ]
