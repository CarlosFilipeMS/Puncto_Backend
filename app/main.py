from fastapi import FastAPI

from app.routes.auth.empresa_auth_routes import auth_empresa_router
from app.routes.empresa_routes import empresa_router
from app.routes.jornada_routes import jornada_router
from app.routes.auth.colaborador_auth_routes import auth_colaborador_router
from app.routes.colaborador_routes import colaborador_router

app = FastAPI()

# AUTH ROUTES
app.include_router(auth_colaborador_router)
app.include_router(auth_empresa_router)

# APP ROUTES
app.include_router(empresa_router)
app.include_router(colaborador_router)
app.include_router(jornada_router)
