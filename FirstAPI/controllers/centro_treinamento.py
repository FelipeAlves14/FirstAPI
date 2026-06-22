"""Controller de Centro de Treinamento."""

# pylint: disable=import-error

from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import LimitOffsetPage, paginate
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from FirstAPI.contrib.dependencies import database_dependency
from FirstAPI.models.CentroTreinamento import CentroTreinamentoModel
from FirstAPI.schemas.centro_treinamento import (
    CentroTreinamentoIn,
    CentroTreinamentoOut,
)

centro_treinamento_router = APIRouter()


@centro_treinamento_router.post(
    "/",
    summary="Criar novo centro de treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: database_dependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:
    """Cria um novo centro de treinamento."""
    try:
        centro_treinamento_out = CentroTreinamentoOut(
            id=uuid4(),
            **centro_treinamento_in.model_dump(),
        )

        centro_treinamento_model = CentroTreinamentoModel(
            **centro_treinamento_out.model_dump()
        )

        db_session.add(centro_treinamento_model)
        await db_session.commit()

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=(
                "JÃ¡ existe um centro de treinamento cadastrado "
                f"com o nome: {centro_treinamento_model.nome}"
            ),
        ) from exc

    return centro_treinamento_out


@centro_treinamento_router.get(
    "/",
    summary="Consultar centros de treinamento",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[CentroTreinamentoOut],
)
async def get(
    db_session: database_dependency,
) -> LimitOffsetPage[CentroTreinamentoOut]:
    """Lista todos os centros de treinamento."""
    centros_treinamento = (
        (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    )

    return paginate(centros_treinamento)


@centro_treinamento_router.get(
    "/{id}",
    summary="Consultar centro de treinamento pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get_by_id(
    centro_treinamento_id: UUID4,
    db_session: database_dependency,
) -> CentroTreinamentoOut:
    """Busca um centro de treinamento pelo ID."""
    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(id=centro_treinamento_id)
            )
        )
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Centro de treinamento nÃ£o encontrado com este ID",
        )

    return centro_treinamento
