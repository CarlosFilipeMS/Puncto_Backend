from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.colaborador_schema import ColaboradorCreateDTO

from app.dependencies.dependencies_sessao import pegar_sessao
from app.services.colaborador_service import (
    criar_colaborador_service,
    listar_todos_colaboradores_service,
    buscar_por_id_service,
    buscar_por_cpf_service,
    buscar_por_nome_service,
)
from app.schemas.colaborador_schema import ColaboradorResponseDTO

colaborador_router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])

@colaborador_router.post("/", response_model=ColaboradorResponseDTO, status_code=201)
def criar_colaborador(dto: ColaboradorCreateDTO, session: Session = Depends(pegar_sessao)):
    return criar_colaborador_service(dto, session)

@colaborador_router.get("/", response_model=List[ColaboradorResponseDTO])
def listar_todos_colaboradores(session: Session = Depends(pegar_sessao)):
    return listar_todos_colaboradores_service(session)

@colaborador_router.get("/{colaborador_id}", response_model=ColaboradorResponseDTO)
def buscar_colaborador_por_id(colaborador_id: UUID, session: Session = Depends(pegar_sessao)):
    return buscar_por_id_service(session, colaborador_id)

@colaborador_router.get("/cpf/{cpf}", response_model=ColaboradorResponseDTO)
def buscar_colaborador_por_cpf(cpf: str, session: Session = Depends(pegar_sessao)):
    return buscar_por_cpf_service(session, cpf)

@colaborador_router.get("/nome/{nome}", response_model=list[ColaboradorResponseDTO])
def buscar_colaborador_por_nome(nome: str, session: Session = Depends(pegar_sessao)):
    return buscar_por_nome_service(session, nome)
