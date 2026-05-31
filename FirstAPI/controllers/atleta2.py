from fastapi import APIRouter, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from FirstAPI.contrib.dependencies import database_dependency
from FirstAPI.models.Atleta import AtletaModel

atleta2_router = APIRouter()

@atleta2_router.delete(
    "/{id}",
    summary="Excluir atleta",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: UUID4, db_session: database_dependency) -> None:
    atleta = (
        await db_session.execute(
            select(AtletaModel).filter_by(id=id)
        )
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Atleta não encontrado pelo ID",
        )

    await db_session.delete(atleta)
    await db_session.commit()