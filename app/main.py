from fastapi import FastAPI

from app.routes.auth.empresa_auth_routes import auth_empresa_router
from app.routes.empresa_routes import empresa_router

app = FastAPI()

from app.routes.auth.auth_routes import auth_router
from app.routes.colaborador_routes import colaborador_router

app.include_router(empresa_router)
app.include_router(auth_empresa_router)
app.include_router(auth_router)
app.include_router(colaborador_router)


