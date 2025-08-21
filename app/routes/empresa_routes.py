from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.dependencies.dependencies_sessao import pegar_sessao
from app.schemas.empresa_schema import EmpresaCreateDTO, EmpresaResponseDTO
from app.services.empresa_service import (
    criar_empresa_service,
    listar_empresas_service,
    listar_empresas_ativas_service,
    buscar_empresa_por_id_service,
    buscar_empresa_por_email_service,
    buscar_empresa_por_cnpj_service,
    atualizar_empresa_service,
    atualizar_status_empresa_service
)
from app.models.empresa import Status

empresa_router = APIRouter(prefix="/empresas", tags=["Empresas"])

# Criar empresa
@empresa_router.post("/", response_model=EmpresaResponseDTO, status_code=201)
def criar_empresa(dto: EmpresaCreateDTO, session: Session = Depends(pegar_sessao)):
    return criar_empresa_service(dto, session)

# Listar todas as empresas
@empresa_router.get("/", response_model=List[EmpresaResponseDTO])
def listar_empresas(session: Session = Depends(pegar_sessao)):
    return listar_empresas_service(session)

# Listar apenas empresas ativas
@empresa_router.get("/ativas", response_model=List[EmpresaResponseDTO])
def listar_empresas_ativas(session: Session = Depends(pegar_sessao)):
    return listar_empresas_ativas_service(session)

# Buscar empresa por ID
@empresa_router.get("/{empresa_id}", response_model=EmpresaResponseDTO)
def buscar_empresa_por_id(empresa_id: UUID, session: Session = Depends(pegar_sessao)):
    return buscar_empresa_por_id_service(empresa_id, session)

# Buscar empresa por CNPJ
@empresa_router.get("/cnpj/{cnpj}", response_model=EmpresaResponseDTO)
def buscar_empresa_por_cnpj(cnpj: str, session: Session = Depends(pegar_sessao)):
    return buscar_empresa_por_cnpj_service(session, cnpj)

# Buscar empresa por Email
@empresa_router.get("/email/{email}", response_model=EmpresaResponseDTO)
def buscar_empresa_por_email(email: str, session: Session = Depends(pegar_sessao)):
    return buscar_empresa_por_email_service(session, email)

# Atualizar empresa
@empresa_router.put("/{empresa_id}", response_model=EmpresaResponseDTO)
def atualizar_empresa(
    empresa_id: UUID,
    dto: EmpresaCreateDTO,
    atualizar_senha: bool = False,
    session: Session = Depends(pegar_sessao)
):
    """
    Atualiza os dados de uma empresa.
    Se atualizar_senha=True, a senha será atualizada com a fornecida no DTO.
    """
    return atualizar_empresa_service(empresa_id, dto, atualizar_senha, session)

# Atualizar status da empresa
@empresa_router.patch("/{empresa_id}/status", response_model=EmpresaResponseDTO)
def atualizar_status_empresa(
    empresa_id: UUID,
    status: Status = Body(..., embed=True),
    session: Session = Depends(pegar_sessao)
):
    """
    Atualiza o status da empresa (ativo/inativo).
    """
    return atualizar_status_empresa_service(session, empresa_id, status)
