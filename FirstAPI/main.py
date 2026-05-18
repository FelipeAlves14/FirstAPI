from fastapi import FastAPI
from fastapi_pagination import add_pagination
from FirstAPI.routers import api_router
import sys

app = FastAPI(title="Primeira construção de API")
app.include_router(api_router)
add_pagination(app)
