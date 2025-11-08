from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from app.models.jornada import Jornada, HorarioJornada
from app.repositories.jornada_repository import salvar_horario, deletar_horario
from app.schemas.jornada_schema import HorarioJornadaCreateDTO, HorarioJornadaUpdateDTO

# Criar horário de jornada
def criar_horario_service(session: Session, jornada_id: UUID, dto: HorarioJornadaCreateDTO, jornada: Jornada = None):
    if jornada is None:
        jornada = session.query(Jornada).filter(Jornada.id == jornada_id).first()
        if not jornada:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada não encontrada")

    horario = HorarioJornada(
        dia_semana=dto.dia_semana,
        hora_inicio=dto.hora_inicio,
        hora_fim=dto.hora_fim,
        jornada=jornada
    )
    return salvar_horario(session, horario)

# Listar horários de uma jornada
def listar_horarios_service(session: Session, jornada_id: UUID):
    jornada = session.query(Jornada).filter(Jornada.id == jornada_id).first()
    if not jornada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada não encontrada")
    return jornada.horarios

# Atualizar horário
def atualizar_horario_service(session: Session, horario_id: UUID, dto: HorarioJornadaUpdateDTO):
    horario = session.query(HorarioJornada).filter(HorarioJornada.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horário não encontrado")

    if dto.dia_semana is not None:
        horario.dia_semana = dto.dia_semana
    if dto.hora_inicio is not None:
        horario.hora_inicio = dto.hora_inicio
    if dto.hora_fim is not None:
        horario.hora_fim = dto.hora_fim

    session.commit()
    session.refresh(horario)
    return horario

# Deletar horário
def deletar_horario_service(session: Session, horario_id: UUID):
    horario = session.query(HorarioJornada).filter(HorarioJornada.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horário não encontrado")
    deletar_horario(session, horario)
    return {"detail": "Horário deletado com sucesso"}
