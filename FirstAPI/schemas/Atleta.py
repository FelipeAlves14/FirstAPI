"""
Schemas relacionados aos atletas.
"""

from typing import Annotated, Optional

from pydantic import Field, PositiveFloat

from FirstAPI.contrib.BaseSchema import BaseSchema, OutMixin
from FirstAPI.schemas.categoria import CategoriaIn
from FirstAPI.schemas.centro_treinamento import CentroTreinamentoAtleta


class Atleta(BaseSchema):
    """Schema base de atleta."""

    nome: Annotated[
        str,
        Field(
            description="Nome do atleta",
            examples=["Felipe"],
            max_length=50,
        ),
    ]

    cpf: Annotated[
        str,
        Field(
            description="CPF do atleta",
            examples=["12345678900"],
            max_length=11,
        ),
    ]

    idade: Annotated[
        int,
        Field(
            description="Idade do atleta",
            examples=[19],
        ),
    ]

    peso: Annotated[
        PositiveFloat,
        Field(
            description="Peso do atleta",
            examples=[49.0],
        ),
    ]

    altura: Annotated[
        PositiveFloat,
        Field(
            description="Altura do atleta",
            examples=[1.65],
        ),
    ]

    sexo: Annotated[
        str,
        Field(
            description="Sexo do atleta",
            examples=["M"],
            max_length=1,
        ),
    ]

    categoria: Annotated[
        CategoriaIn,
        Field(
            description="Categoria do atleta",
        ),
    ]

    centro_treinamento: Annotated[
        CentroTreinamentoAtleta,
        Field(
            description="Centro de treinamento do atleta",
        ),
    ]


class AtletaIn(Atleta):
    """Schema para criação de atleta."""


class AtletaOut(AtletaIn, OutMixin):
    """Schema de retorno de atleta."""


class AtletaUpdate(BaseSchema):
    """Schema para atualização de atleta."""

    nome: Annotated[
        Optional[str],
        Field(
            description="Nome do atleta",
            examples=["Felipe"],
            max_length=50,
        ),
    ]

    idade: Annotated[
        Optional[int],
        Field(
            description="Idade do atleta",
            examples=[19],
        ),
    ]


class AtletaOutGetAll(BaseSchema):
    """Schema para listagem de atletas."""

    nome: Annotated[
        str,
        Field(
            description="Nome do atleta",
            examples=["Felipe"],
            max_length=50,
        ),
    ]

    categoria: Annotated[
        CategoriaIn,
        Field(
            description="Categoria do atleta",
        ),
    ]

    centro_treinamento: Annotated[
        CentroTreinamentoAtleta,
        Field(
            description="Centro de treinamento do atleta",
        ),
    ]
