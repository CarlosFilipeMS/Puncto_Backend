from fastapi import FastAPI

app = FastAPI()

from app.routes.auth_routes import auth_router
from app.routes.colaborador_routes import colaborador_router

app.include_router(auth_router)
app.include_router(colaborador_router)


