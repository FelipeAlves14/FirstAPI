"""
Controller responsável pelas operações relacionadas às categorias.
"""

from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import LimitOffsetPage, paginate
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from FirstAPI.contrib.dependencies import database_dependency
from FirstAPI.models.Categoria import CategoriaModel
from FirstAPI.schemas.Categoria import CategoriaIn, CategoriaOut

categoria_router = APIRouter()


@categoria_router.post(
    "/",
    summary="Criar nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: database_dependency,
    categoria_in: CategoriaIn = Body(...),
) -> CategoriaOut:
    """
    Cria uma nova categoria.
    """
    try:
        categoria_out = CategoriaOut(
            id=uuid4(),
            **categoria_in.model_dump(),
        )

        categoria_model = CategoriaModel(
            **categoria_out.model_dump()
        )

        db_session.add(categoria_model)
        await db_session.commit()

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=(
                "Já existe uma categoria cadastrada "
                f"com o nome: {categoria_model.nome}"
            ),
        ) from exc

    return categoria_out


@categoria_router.get(
    "/",
    summary="Consultar categorias",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[CategoriaOut],
)
async def get(
    db_session: database_dependency,
) -> LimitOffsetPage[CategoriaOut]:
    """
    Retorna todas as categorias cadastradas.
    """
    categorias: list[CategoriaOut] = (
        (
            await db_session.execute(
                select(CategoriaModel)
            )
        )
        .scalars()
        .all()
    )

    return paginate(categorias)


@categoria_router.get(
    "/{categoria_id}",
    summary="Consultar categoria pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get_by_id(
    categoria_id: UUID4,
    db_session: database_dependency,
) -> CategoriaOut:
    """
    Retorna uma categoria pelo ID.
    """
    categoria: CategoriaOut = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(
                    id=categoria_id
                )
            )
        )
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada com este ID",
        )

    return categoria
