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

# Criar colaborador
@colaborador_router.post("/", response_model=ColaboradorResponseDTO, status_code=201)
def criar_colaborador(dto: ColaboradorCreateDTO, session: Session = Depends(pegar_sessao)):
    return criar_colaborador_service(dto, session)

# Listar todos os colaboradores
@colaborador_router.get("/", response_model=List[ColaboradorResponseDTO])
def listar_todos_colaboradores(session: Session = Depends(pegar_sessao)):
    # empresa_id será obtido do token depois
    return listar_todos_colaboradores_service(session)

# Listar apenas colaboradores ativos
@colaborador_router.get("/ativos", response_model=List[ColaboradorResponseDTO])
def listar_colaboradores_ativos(session: Session = Depends(pegar_sessao)):
    # empresa_id será obtido do token depois
    return listar_colaboradores_ativos_service(session)

# Buscar colaborador por ID
@colaborador_router.get("/{colaborador_id}", response_model=ColaboradorResponseDTO)
def buscar_colaborador_por_id(
    colaborador_id: UUID,
    session: Session = Depends(pegar_sessao)
):
    return buscar_por_id_service(session, colaborador_id)

# Buscar colaborador por CPF
@colaborador_router.get("/cpf/{cpf}", response_model=ColaboradorResponseDTO)
def buscar_colaborador_por_cpf(cpf: str, session: Session = Depends(pegar_sessao)):
    return buscar_por_cpf_service(session, cpf)

# Buscar colaborador por nome
@colaborador_router.get("/nome/{nome}", response_model=List[ColaboradorResponseDTO])
def buscar_colaborador_por_nome(nome: str, session: Session = Depends(pegar_sessao)):
    return buscar_por_nome_service(session, nome)

# Atualizar dados do colaborador (nome, cargo, jornada, senha)
@colaborador_router.put("/{colaborador_id}", response_model=ColaboradorResponseDTO)
def atualizar_colaborador(
    colaborador_id: UUID,
    dto: ColaboradorUpdateDTO,
    session: Session = Depends(pegar_sessao)
):
    return atualizar_colaborador_service(session, colaborador_id, dto)

# Atualizar status ou role do colaborador
@colaborador_router.patch("/{colaborador_id}/status-role", response_model=ColaboradorResponseDTO)
def atualizar_status_e_role_colaborador(
    colaborador_id: UUID,
    dto: ColaboradorUpdateStatusRoleDTO,
    session: Session = Depends(pegar_sessao)
):
    return atualizar_status_role_colaborador_service(
        session,
        colaborador_id,
        status=dto.status,
        role=dto.role
    )
