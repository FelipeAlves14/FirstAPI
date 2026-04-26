from uuid import uuid4
from fastapi_pagination import LimitOffsetPage, paginate
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from FirstAPI.contrib.dependencies import database_dependency
from FirstAPI.schemas.CentroTreinamento import CentroTreinamentoIn, CentroTreinamentoOut
from FirstAPI.models.CentroTreinamento import CentroTreinamentoModel

centro_treinamento_router = APIRouter()


@centro_treinamento_router.post(
    "/",
    summary="Criar novo centro de treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: database_dependency, centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    try:
        centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
        db_session.add(centro_treinamento_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
                            detail=f"Já existe um centro de treinamento cadastrado com o nome: {centro_treinamento_model.nome}")
    return centro_treinamento_out


@centro_treinamento_router.get(
    "/",
    summary="Consultar centros de treinamento",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[CentroTreinamentoOut],
)
async def get(db_session: database_dependency) -> LimitOffsetPage[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return paginate(centros_treinamento)


@centro_treinamento_router.get(
    "/{id}",
    summary="Consultar centro de treinamento pelo ID",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get_by_id(id: UUID4, db_session: database_dependency) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Centro de treinamento não encontrado com este ID")
    return centro_treinamento