from sqlalchemy.orm import Session
from uuid import UUID
from app.models.colaborador import Colaborador, Status
from app.roles import Role

# REPOSITORY

def salvar_colaborador(dto, senha_hash: str, session: Session, empresa_id: UUID):
    colaborador = Colaborador(
        nome=dto.nome,
        email=dto.email,
        cpf=dto.cpf,
        cargo=dto.cargo,
        empresa_id=empresa_id,
        jornada_id=dto.jornada_id,
        senha_hash=senha_hash
    )
    session.add(colaborador)
    session.commit()
    session.refresh(colaborador)
    return colaborador


def listar_todos(session: Session, empresa_id: UUID):
    return session.query(Colaborador).filter(Colaborador.empresa_id == empresa_id).all()

def listar_todos_ativos(session: Session, empresa_id: UUID):
    return session.query(Colaborador).filter(
        Colaborador.empresa_id == empresa_id,
        Colaborador.status == Status.ATIVO
    ).all()

def buscar_por_id_e_empresa(session: Session, id: UUID, empresa_id: UUID):
    return session.query(Colaborador).filter(
        Colaborador.id == id,
        Colaborador.empresa_id == empresa_id
    ).first()

def buscar_por_cpf_e_empresa(session: Session, cpf: str, empresa_id: UUID):
    return session.query(Colaborador).filter(
        Colaborador.cpf == cpf,
        Colaborador.empresa_id == empresa_id
    ).first()

def buscar_por_nome(session: Session, nome: str, empresa_id: UUID | None = None):
    query = session.query(Colaborador).filter(Colaborador.nome.ilike(f"%{nome}%"))
    if empresa_id:
        query = query.filter(Colaborador.empresa_id == empresa_id)
    return query.all()

def buscar_por_email_e_empresa(session: Session, email: str, empresa_id: UUID):
    return session.query(Colaborador).filter(
        Colaborador.email == email,
        Colaborador.empresa_id == empresa_id
    ).first()

def atualizar_status_e_role_colaborador(session: Session, colaborador_id: UUID, status: Status | None = None, role: Role | None = None):
    colaborador = session.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
    if not colaborador:
        return None
    if status:
        colaborador.status = status
    if role:
        colaborador.role = role
    session.commit()
    session.refresh(colaborador)
    return colaborador
