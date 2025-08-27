from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.dependencies.dependencies_sessao import pegar_sessao
from app.services.jornada_service import (
    criar_jornada_service,
    listar_jornadas_service,
    buscar_jornada_service,
    atualizar_jornada_service,
    deletar_jornada_service
)
from app.services.horario_jornada_service import (
    criar_horario_service,
    listar_horarios_service,
    atualizar_horario_service,
    deletar_horario_service
)
from app.schemas.jornada_schema import (
    JornadaCreateDTO, JornadaUpdateDTO, JornadaResponseDTO,
    HorarioJornadaCreateDTO, HorarioJornadaUpdateDTO, HorarioJornadaResponseDTO
)

jornada_router = APIRouter(prefix="/jornadas", tags=["Jornadas"])

# ----------------- Rotas Jornada -----------------
@jornada_router.post("/", response_model=JornadaResponseDTO, status_code=201)
def criar_jornada(dto: JornadaCreateDTO, session: Session = Depends(pegar_sessao)):
    return criar_jornada_service(dto, session)

@jornada_router.get("/", response_model=List[JornadaResponseDTO])
def listar_jornadas(empresa_id: UUID, session: Session = Depends(pegar_sessao)):
    return listar_jornadas_service(session, empresa_id)

@jornada_router.get("/{jornada_id}", response_model=JornadaResponseDTO)
def buscar_jornada(jornada_id: UUID, session: Session = Depends(pegar_sessao)):
    return buscar_jornada_service(session, jornada_id)

@jornada_router.put("/{jornada_id}", response_model=JornadaResponseDTO)
def atualizar_jornada(jornada_id: UUID, dto: JornadaUpdateDTO, session: Session = Depends(pegar_sessao)):
    return atualizar_jornada_service(session, jornada_id, dto)

@jornada_router.delete("/{jornada_id}")
def deletar_jornada(jornada_id: UUID, session: Session = Depends(pegar_sessao)):
    return deletar_jornada_service(session, jornada_id)

# ----------------- Rotas Horário -----------------
@jornada_router.post("/{jornada_id}/horarios", response_model=HorarioJornadaResponseDTO, status_code=201)
def criar_horario(jornada_id: UUID, dto: HorarioJornadaCreateDTO, session: Session = Depends(pegar_sessao)):
    return criar_horario_service(session, jornada_id, dto)

@jornada_router.get("/{jornada_id}/horarios", response_model=List[HorarioJornadaResponseDTO])
def listar_horarios(jornada_id: UUID, session: Session = Depends(pegar_sessao)):
    return listar_horarios_service(session, jornada_id)

@jornada_router.put("/horarios/{horario_id}", response_model=HorarioJornadaResponseDTO)
def atualizar_horario(horario_id: UUID, dto: HorarioJornadaUpdateDTO, session: Session = Depends(pegar_sessao)):
    return atualizar_horario_service(session, horario_id, dto)

@jornada_router.delete("/horarios/{horario_id}")
def deletar_horario(horario_id: UUID, session: Session = Depends(pegar_sessao)):
    return deletar_horario_service(session, horario_id)