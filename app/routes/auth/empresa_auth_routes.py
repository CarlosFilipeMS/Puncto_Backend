from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.dependencies_sessao import pegar_sessao
from app.schemas.empresa_schema import EmpresaLoginDTO
from app.services.empresa_service import login_empresa_service

auth_empresa_router = APIRouter(prefix="/auth/empresa", tags=["Auth Empresa"])

@auth_empresa_router.post("/login")
def login_empresa(dto: EmpresaLoginDTO, session: Session = Depends(pegar_sessao)):
    """
    Endpoint de login da empresa.
    Chama o service que valida CNPJ, senha e retorna JWT.
    """
    return login_empresa_service(dto, session)
