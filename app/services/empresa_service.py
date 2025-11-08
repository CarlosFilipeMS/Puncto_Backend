# app/services/empresa_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.schemas.empresa_schema import EmpresaCreateDTO, EmpresaLoginDTO
from app.repositories.empresa_repository import (
    salvar_empresa,
    buscar_por_id,
    buscar_por_cnpj,
    buscar_por_email,
    listar_todas_empresas,
    listar_todas_empresas_ativas,
    atualizar_empresa,
    atualizar_status
)
from app.utils.jwt import criar_token_jwt
from app.utils.security import gerar_hash_senha, verificar_senha
from app.models.empresa import Status


# ----------------- CRUD -----------------

def criar_empresa_service(session: Session, dto: EmpresaCreateDTO):
    """Cria uma nova empresa após validar CNPJ único."""
    if buscar_por_cnpj(session, dto.cnpj):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CNPJ já cadastrado")

    senha_hash = gerar_hash_senha(dto.senha)
    return salvar_empresa(dto, senha_hash, session)


def listar_empresas_service(session: Session):
    """Lista todas as empresas, incluindo inativas."""
    return listar_todas_empresas(session)


def listar_empresas_ativas_service(session: Session):
    """Lista apenas empresas ativas."""
    return listar_todas_empresas_ativas(session)


def buscar_empresa_por_id_service(session: Session, empresa_id: UUID):
    """Busca empresa por ID."""
    empresa = buscar_por_id(session, empresa_id)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa


def buscar_empresa_por_email_service(session: Session, email: str):
    """Busca empresa por e-mail."""
    empresa = buscar_por_email(session, email)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa


def buscar_empresa_por_cnpj_service(session: Session, cnpj: str):
    """Busca empresa por CNPJ."""
    empresa = buscar_por_cnpj(session, cnpj)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa


def atualizar_empresa_service(session: Session, empresa_id: UUID, dto: EmpresaCreateDTO, atualizar_senha: bool = False):
    """Atualiza os dados da empresa, opcionalmente atualizando a senha."""
    senha_hash = gerar_hash_senha(dto.senha) if atualizar_senha else None
    empresa = atualizar_empresa(session, empresa_id, dto, senha_hash)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa


def atualizar_status_empresa_service(session: Session, empresa_id: UUID, status: Status):
    """Atualiza o status da empresa (ativo/inativo)."""
    empresa = atualizar_status(session, empresa_id, status)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa

def login_empresa_service(dto: EmpresaLoginDTO, session: Session):
    """Valida login da empresa e retorna JWT."""
    empresa = buscar_por_cnpj(session, dto.cnpj)

    if not empresa or not verificar_senha(dto.senha, empresa.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CNPJ ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # em empresa_service.py
    token = criar_token_jwt(subject=str(empresa.id), additional_claims={"empresa_id": str(empresa.id)})

    return {"access_token": token, "token_type": "bearer"}
