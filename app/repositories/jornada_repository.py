from sqlalchemy.orm import Session
from app.models.jornada import Jornada, HorarioJornada
from uuid import UUID

# Jornada
def salvar_jornada(session: Session, jornada: Jornada):
    session.add(jornada)
    session.commit()
    session.refresh(jornada)
    return jornada

def listar_todas_jornadas(session: Session, empresa_id: UUID):
    return session.query(Jornada).filter(Jornada.empresa_id == empresa_id).all()

def buscar_jornada_por_id(session: Session, jornada_id: UUID):
    return session.query(Jornada).filter(Jornada.id == jornada_id).first()

def deletar_jornada(session: Session, jornada: Jornada):
    session.delete(jornada)
    session.commit()

# Horário Jornada
def salvar_horario(session: Session, horario: HorarioJornada):
    session.add(horario)
    session.commit()
    session.refresh(horario)
    return horario

def deletar_horario(session: Session, horario: HorarioJornada):
    session.delete(horario)
    session.commit()
