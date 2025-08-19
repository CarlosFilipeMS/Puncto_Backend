from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.dependencies_sessao import pegar_sessao
from app.schemas.empresa_schema import EmpresaLoginDTO
from app.services.empresa_service import buscar_empresa_por_cnpj_service
from app.utils.security import verificar_senha
from app.utils.jwt import criar_token_jwt

auth_empresa_router = APIRouter(prefix="/auth/empresa", tags=["Auth Empresa"])

@auth_empresa_router.post("/login")
def login_empresa(dto: EmpresaLoginDTO, session: Session = Depends(pegar_sessao)):
    empresa = buscar_empresa_por_cnpj_service(session, dto.cnpj)

    if not verificar_senha(dto.senha, empresa.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CNPJ ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = criar_token_jwt(empresa.id)
    return {"access_token": token, "token_type": "bearer"}
