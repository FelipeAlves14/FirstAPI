from datetime import datetime
from fastapi_pagination.utils import disable_installed_extensions_check
from fastapi_pagination import LimitOffsetPage, paginate
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from FirstAPI.contrib.dependencies import database_dependency
from FirstAPI.schemas.Atleta import AtletaIn, AtletaOut, AtletaOutGetAll, AtletaUpdate
from FirstAPI.models.Atleta import AtletaModel
from FirstAPI.models.Categoria import CategoriaModel
from FirstAPI.models.CentroTreinamento import CentroTreinamentoModel
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

disable_installed_extensions_check()
atleta_router = APIRouter()

@atleta_router.post("/", 
    summary="Criar novo atleta", status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,)
async def post(db_session: database_dependency, atleta_in: AtletaIn = Body(...)) -> AtletaOut:
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()
    if not categoria or not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"O atleta não pratica {atleta_in.categoria.nome} ou então não frequenta {atleta_in.centro_treinamento.nome}")
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.strptime(datetime.now().strftime("%d/%m/%y %H:%M:%S"), "%d/%m/%y %H:%M:%S"), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
                            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_model.cpf}")
    return atleta_out

@atleta_router.get("/",
    summary="Consultar atletas",
    response_model=LimitOffsetPage[AtletaOutGetAll],)
async def get(db_session: database_dependency, nome: str = None, cpf: str = None) -> LimitOffsetPage[AtletaOutGetAll]:
    atletas: list[AtletaOutGetAll] = list()
    if nome:
        for atleta in (await db_session.execute(select(AtletaModel).filter_by(nome=nome))).scalars().all():
            atletas.append(atleta)
    if cpf:
        for atleta in (await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))).scalars().all():
            atletas.append(atleta) if atleta not in atletas else None    
    if not nome and not cpf:
        atletas = (await db_session.execute(select(AtletaModel))).scalars().all()
    return paginate(atletas)


@atleta_router.get("/{id}",
    summary="Consultar atleta pelo ID",
    response_model=AtletaOut,)
async def get_by_id(id: UUID4, db_session: database_dependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Atleta não encontrado pelo ID")
    return atleta

@atleta_router.patch("/{id}",
                     summary="Atualizar atleta pelo ID",
                     response_model=AtletaOut,)
async def update(id: UUID4, db_session: database_dependency, atleta_update: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Atleta não encontrado pelo ID")
    for key, value in atleta_update.model_dump(exclude_unset=True).items():
        setattr(atleta, key, value)
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta

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