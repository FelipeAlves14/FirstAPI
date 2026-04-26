from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from FirstAPI.configs.database import get_session

database_dependency = Annotated[AsyncSession, Depends(get_session)]