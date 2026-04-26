from typing import Annotated

from pydantic import UUID4, Field
from FirstAPI.contrib.BaseSchema import BaseSchema

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", examples=["Futebol"], max_length=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description="ID")]