from typing import Annotated

from pydantic import UUID4, Field
from FirstAPI.contrib.BaseSchema import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", examples=["PG Fit"], max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", examples=["Rua dali numero de la"], max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietário centro de treinamento", examples=["Felipão"], max_length=30)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description="ID")]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", examples=["PG Fit"], max_length=20)]
