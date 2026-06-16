# pylint: disable=too-few-public-methods

"""
Schemas relacionados ao Centro de Treinamento.
"""

from typing import Annotated

from pydantic import UUID4, Field

from FirstAPI.contrib.BaseSchema import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    """Schema para criação de um centro de treinamento."""

    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            examples=["PG Fit"],
            max_length=20,
        ),
    ]

    endereco: Annotated[
        str,
        Field(
            description="Endereço do centro de treinamento",
            examples=["Rua dali numero de la"],
            max_length=60,
        ),
    ]

    proprietario: Annotated[
        str,
        Field(
            description="Proprietário do centro de treinamento",
            examples=["Felipão"],
            max_length=30,
        ),
    ]


class CentroTreinamentoOut(CentroTreinamentoIn):
    """Schema de retorno de um centro de treinamento."""

    id: Annotated[UUID4, Field(description="ID")]


class CentroTreinamentoAtleta(BaseSchema):
    """Schema simplificado do centro de treinamento para atletas."""

    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            examples=["PG Fit"],
            max_length=20,
        ),
    ]
