"""
Controlador responsÃ¡vel pelas operaÃ§Ãµes de atletas.
"""

# pylint: disable=duplicate-code,import-error

from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import LimitOffsetPage, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from FirstAPI.contrib.dependencies import database_dependency
from FirstAPI.models.Atleta import AtletaModel
from FirstAPI.models.Categoria import CategoriaModel
from FirstAPI.models.CentroTreinamento import CentroTreinamentoModel
from FirstAPI.schemas.Atleta import (
    AtletaIn,
    AtletaOut,
    AtletaOutGetAll,
    AtletaUpdate,
)

disable_installed_extensions_check()

atleta_router = APIRouter()


async def get_atleta_by_id(
    atleta_id: UUID4,
    db_session: database_dependency,
) -> AtletaModel | None:
    """
    Busca um atleta pelo ID.
    """
    return (
        await db_session.execute(
            select(AtletaModel).filter_by(id=atleta_id)
        )
    ).scalars().first()


@atleta_router.post(
    "/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: database_dependency,
    atleta_in: AtletaIn = Body(...),
) -> AtletaOut:
    """
    Cria um novo atleta.
    """
    categoria = (
        await db_session.execute(
            select(CategoriaModel).filter_by(
                nome=atleta_in.categoria.nome
            )
        )
    ).scalars().first()

    centro_treinamento = (
        await db_session.execute(
            select(CentroTreinamentoModel).filter_by(
                nome=atleta_in.centro_treinamento.nome
            )
        )
    ).scalars().first()

    if not categoria or not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"O atleta nÃ£o pratica "
                f"{atleta_in.categoria.nome} "
                f"ou nÃ£o frequenta "
                f"{atleta_in.centro_treinamento.nome}"
            ),
        )

    try:
        atleta_out = AtletaOut(
            id=uuid4(),
            created_at=datetime.now(),
            **atleta_in.model_dump(),
        )

        atleta_model = AtletaModel(
            **atleta_out.model_dump(
                exclude={
                    "categoria",
                    "centro_treinamento",
                }
            )
        )

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = (
            centro_treinamento.pk_id
        )

        db_session.add(atleta_model)
        await db_session.commit()

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=(
                "JÃ¡ existe um atleta "
                f"cadastrado com o cpf: "
                f"{atleta_model.cpf}"
            ),
        ) from exc

    return atleta_out


@atleta_router.get(
    "/",
    summary="Consultar atletas",
    response_model=LimitOffsetPage[AtletaOutGetAll],
)
async def get(
    db_session: database_dependency,
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
) -> LimitOffsetPage[AtletaOutGetAll]:
    """
    Consulta atletas por nome, CPF ou retorna todos.
    """
    atletas: list[AtletaOutGetAll] = []

    if nome:
        resultado = await db_session.execute(
            select(AtletaModel).filter_by(nome=nome)
        )

        for atleta in resultado.scalars().all():
            atletas.append(atleta)

    if cpf:
        resultado = await db_session.execute(
            select(AtletaModel).filter_by(cpf=cpf)
        )

        for atleta in resultado.scalars().all():
            if atleta not in atletas:
                atletas.append(atleta)

    if not nome and not cpf:
        atletas = (
            await db_session.execute(
                select(AtletaModel)
            )
        ).scalars().all()

    return paginate(atletas)


@atleta_router.get(
    "/{atleta_id}",
    summary="Consultar atleta pelo ID",
    response_model=AtletaOut,
)
async def get_by_id(
    atleta_id: UUID4,
    db_session: database_dependency,
) -> AtletaOut:
    """
    Consulta um atleta pelo ID.
    """
    atleta = await get_atleta_by_id(
        atleta_id,
        db_session,
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atleta nÃ£o encontrado pelo ID",
        )

    return atleta


@atleta_router.patch(
    "/{atleta_id}",
    summary="Atualizar atleta pelo ID",
    response_model=AtletaOut,
)
async def update(
    atleta_id: UUID4,
    db_session: database_dependency,
    atleta_update: AtletaUpdate = Body(...),
) -> AtletaOut:
    """
    Atualiza um atleta pelo ID.
    """
    atleta = await get_atleta_by_id(
        atleta_id,
        db_session,
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Atleta nÃ£o encontrado pelo ID",
        )

    for key, value in atleta_update.model_dump(
        exclude_unset=True
    ).items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@atleta_router.delete(
    "/{atleta_id}",
    summary="Excluir atleta",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    atleta_id: UUID4,
    db_session: database_dependency,
) -> None:
    """
    Exclui um atleta pelo ID.
    """
    atleta = await get_atleta_by_id(
        atleta_id,
        db_session,
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Atleta nÃ£o encontrado pelo ID",
        )

    await db_session.delete(atleta)
    await db_session.commit()
