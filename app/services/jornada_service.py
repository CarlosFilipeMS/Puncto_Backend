from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from app.models.jornada import Jornada, HorarioJornada
from app.repositories.jornada_repository import (
    salvar_jornada,
    listar_todas_jornadas,
    buscar_jornada_por_id,
    deletar_jornada,
    salvar_horario,
    deletar_horario
)
from app.schemas.jornada_schema import JornadaCreateDTO, JornadaUpdateDTO

# Criar jornada com horários
def criar_jornada_service(dto: JornadaCreateDTO, session: Session):
    jornada = Jornada(
        nome=dto.nome,
        horas_semanais=dto.horas_semanais,
        empresa_id=dto.empresa_id
    )

    # Criar horários
    for h in dto.horarios:
        horario = HorarioJornada(
            dia_semana=h.dia_semana,
            hora_inicio=h.hora_inicio,
            hora_fim=h.hora_fim
        )
        jornada.horarios.append(horario)

    return salvar_jornada(session, jornada)

# Listar todas as jornadas de uma empresa
def listar_jornadas_service(session: Session, empresa_id: UUID):
    return listar_todas_jornadas(session, empresa_id)

# Buscar jornada por ID
def buscar_jornada_service(session: Session, jornada_id: UUID):
    jornada = buscar_jornada_por_id(session, jornada_id)
    if not jornada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada não encontrada")
    return jornada

# Atualizar jornada
def atualizar_jornada_service(session: Session, jornada_id: UUID, dto: JornadaUpdateDTO):
    jornada = buscar_jornada_por_id(session, jornada_id)
    if not jornada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada não encontrada")

    if dto.nome:
        jornada.nome = dto.nome
    if dto.horas_semanais:
        jornada.horas_semanais = dto.horas_semanais

    # Atualizar horários
    if dto.horarios is not None:
        # Deletar antigos
        for h in jornada.horarios:
            deletar_horario(session, h)
        jornada.horarios.clear()

        # Adicionar novos
        for h in dto.horarios:
            horario = HorarioJornada(
                dia_semana=h.dia_semana,
                hora_inicio=h.hora_inicio,
                hora_fim=h.hora_fim
            )
            jornada.horarios.append(horario)

    session.commit()
    session.refresh(jornada)
    return jornada

# Deletar jornada
def deletar_jornada_service(session: Session, jornada_id: UUID):
    jornada = buscar_jornada_por_id(session, jornada_id)
    if not jornada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada não encontrada")
    deletar_jornada(session, jornada)
    return {"detail": "Jornada deletada com sucesso"}
