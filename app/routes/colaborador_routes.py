from typing import List
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.colaborador_schema import (
    ColaboradorCreateDTO,
    ColaboradorResponseDTO,
    ColaboradorUpdateDTO,
    ColaboradorUpdateStatusRoleDTO
)
from app.dependencies.dependencies_sessao import pegar_sessao
from app.dependencies.dependencies_token import get_empresa_id_from_token
from app.services.colaborador_service import (
    criar_colaborador_service,
    listar_todos_colaboradores_service,
    listar_colaboradores_ativos_service,
    buscar_por_id_service,
    buscar_por_cpf_service,
    buscar_por_nome_service,
    atualizar_colaborador_service,
    atualizar_status_role_colaborador_service
)
from app.models.colaborador import Status, Role

colaborador_router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])

# ----------------- ROTAS PROTEGIDAS -----------------

# Criar colaborador
@colaborador_router.post("/", response_model=ColaboradorResponseDTO, status_code=201)
def criar_colaborador(
    dto: ColaboradorCreateDTO,
    empresa_id: UUID = Depends(get_empresa_id_from_token),
    session: Session = Depends(pegar_sessao)
):
    return criar_colaborador_service(dto, session, empresa_id)

# Listar todos os colaboradores
@colaborador_router.get("/", response_model=List[ColaboradorResponseDTO])
def listar_todos_colaboradores(
    empresa_id: UUID = Depends(get_empresa_id_from_token),
    session: Session = Depends(pegar_sessao)
):
    return listar_todos_colaboradores_service(session, empresa_id)

# Listar apenas colaboradores ativos
@colaborador_router.get("/ativos", response_model=List[ColaboradorResponseDTO])
def listar_colaboradores_ativos(
    empresa_id: UUID = Depends(get_empresa_id_from_token),
    session: Session = Depends(pegar_sessao)
):
    return listar_colaboradores_ativos_service(session, empresa_id)

# Buscar colaborador por ID
@colaborador_router.get("/{colaborador_id}", response_model=ColaboradorResponseDTO)
def buscar_colaborador_por_id(
    colaborador_id: UUID,
    empresa_id: UUID = Depends(get_empresa_id_from_token),
    session: Session = Depends(pegar_sessao)
):
    return buscar_por_id_service(session, colaborador_id, empresa_id)

# Buscar colaborador por CPF
@colaborador_router.get("/cpf/{cpf}", response_model=ColaboradorResponseDTO)
def buscar_colaborador_por_cpf(
    cpf: str,
    empresa_id: UUID = Depends(get_empresa_id_from_token),
    session: Session = Depends(pegar_sessao)
):
    return buscar_por_cpf_service(session, cpf, empresa_id)

# Buscar colaborador por nome
@colaborador_router.get("/nome/{nome}", response_model=List[ColaboradorResponseDTO])
def buscar_colaborador_por_nome(
    nome: str,
    empresa_id: UUID = Depends(get_empresa_id_from_token),
    session: Session = Depends(pegar_sessao)
):
    return buscar_por_nome_service(session, nome, empresa_id)

# Atualizar dados do colaborador (nome, cargo, jornada, senha)
@colaborador_router.put("/{colaborador_id}", response_model=ColaboradorResponseDTO)
def atualizar_colaborador(
    colaborador_id: UUID,
    dto: ColaboradorUpdateDTO,
    empresa_id: UUID = Depends(get_empresa_id_from_token),
    session: Session = Depends(pegar_sessao)
):
    return atualizar_colaborador_service(session, colaborador_id, dto, empresa_id)

# Atualizar status ou role do colaborador
@colaborador_router.patch("/{colaborador_id}/status-role", response_model=ColaboradorResponseDTO)
def atualizar_status_e_role_colaborador(
    colaborador_id: UUID,
    dto: ColaboradorUpdateStatusRoleDTO,
    empresa_id: UUID = Depends(get_empresa_id_from_token),
    session: Session = Depends(pegar_sessao)
):
    return atualizar_status_role_colaborador_service(
        session,
        colaborador_id,
        empresa_id,
        status=dto.status,
        role=dto.role
    )
