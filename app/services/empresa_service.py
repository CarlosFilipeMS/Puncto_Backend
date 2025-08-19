from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.schemas.empresa_schema import EmpresaCreateDTO
from app.repositories.empresa_repository import (
    salvar_empresa,
    buscar_por_id,
    buscar_por_cnpj,
    listar_todas_empresas,
    atualizar_empresa
)
from app.utils.security import gerar_hash_senha

def criar_empresa_service(dto: EmpresaCreateDTO, session: Session):
    # Verifica se já existe uma empresa com o mesmo CNPJ
    if buscar_por_cnpj(session, dto.cnpj):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="CNPJ já cadastrado"
        )

    senha_hash = gerar_hash_senha(dto.senha)
    return salvar_empresa(dto, senha_hash, session)


def listar_empresas_service(session: Session):
    return listar_todas_empresas(session)


def buscar_empresa_por_id_service(session: Session, empresa_id: UUID):
    empresa = buscar_por_id(session, empresa_id)
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    return empresa

def atualizar_empresa_service(empresa_id: UUID, dto: EmpresaCreateDTO, atualizar_senha: bool, session: Session):
    senha_hash = gerar_hash_senha(dto.senha) if atualizar_senha else None
    empresa = atualizar_empresa(session, empresa_id, dto, senha_hash)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa

def buscar_empresa_por_cnpj_service(session: Session, cnpj: str):
    empresa = buscar_por_cnpj(session, cnpj)
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    return empresa
