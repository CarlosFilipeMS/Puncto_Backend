from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.schemas.empresa_schema import EmpresaCreateDTO
from app.repositories.empresa_repository import (
    salvar_empresa,
    buscar_por_id,
    buscar_por_cnpj,
    buscar_por_email,
    listar_todas_empresas,
    atualizar_empresa,
    listar_todas_empresas_ativas,
    atualizar_status
)
from app.utils.security import gerar_hash_senha
from app.models.empresa import Status

def criar_empresa_service(dto: EmpresaCreateDTO, session: Session):
    if buscar_por_cnpj(session, dto.cnpj):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CNPJ já cadastrado")

    senha_hash = gerar_hash_senha(dto.senha)
    return salvar_empresa(dto, senha_hash, session)


def listar_empresas_service(session: Session):
    return listar_todas_empresas(session)

def listar_empresas_ativas_service(session: Session):
    return listar_todas_empresas_ativas(session)

def buscar_empresa_por_id_service(empresa_id: UUID, session: Session):
    empresa = buscar_por_id(session, empresa_id)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa

def buscar_empresa_por_email_service(session: Session, email: str):
    empresa = buscar_por_email(session, email)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa

def buscar_empresa_por_cnpj_service(session: Session, cnpj: str):
    empresa = buscar_por_cnpj(session, cnpj)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa

def atualizar_empresa_service(empresa_id: UUID, dto: EmpresaCreateDTO, atualizar_senha: bool, session: Session):
    senha_hash = gerar_hash_senha(dto.senha) if atualizar_senha else None
    empresa = atualizar_empresa(session, empresa_id, dto, senha_hash)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa

def atualizar_status_empresa_service(session: Session, empresa_id: UUID, status: Status):
    empresa = atualizar_status(session, empresa_id, status)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa
