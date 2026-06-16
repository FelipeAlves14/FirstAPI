"""FastAPI application entrypoint."""

# pylint: disable=import-error

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from FirstAPI.routers import api_router

app = FastAPI(title="Primeira construcao de API")
app.include_router(api_router)
add_pagination(app)
