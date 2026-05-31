from uuid import uuid4
from fastapi_pagination import LimitOffsetPage, paginate
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from FirstAPI.contrib.dependencies import database_dependency
from FirstAPI.schemas.Categoria import CategoriaIn, CategoriaOut
from FirstAPI.models.Categoria import CategoriaModel

categoria_router = APIRouter()


@categoria_router.post(
    "/",
    summary="Criar nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: database_dependency, categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    try:
        categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
        categoria_model = CategoriaModel(**categoria_out.model_dump())
        db_session.add(categoria_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
                            detail=f"Já existe uma categoria cadastrada com o nome: {categoria_model.nome}")
    return categoria_out


@categoria_router.get(
    "/",
    summary="Consultar categorias",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[CategoriaOut],
)
async def get(db_session: database_dependency) -> LimitOffsetPage[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return paginate(categorias)


@categoria_router.get(
    "/{id}",
    summary="Consultar categoria pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get_by_id(id: UUID4, db_session: database_dependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Categoria não encontrada com este ID")
    return categoria


@atleta_router.delete("/{id}",
                      summary="Excluir atleta",
                      status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db_session: database_dependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Atleta não encontrado pelo ID")
    await db_session.delete(atleta)
    await db_session.commit()