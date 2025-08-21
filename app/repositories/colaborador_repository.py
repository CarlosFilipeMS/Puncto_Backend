from sqlalchemy.orm import Session
from uuid import UUID
from app.models.colaborador import Colaborador, Status
from app.schemas.colaborador_schema import ColaboradorCreateDTO
from app.roles import Role

def salvar_colaborador(dto: ColaboradorCreateDTO, senha_hash: str, session: Session):
    colaborador = Colaborador(
        nome=dto.nome,
        cpf=dto.cpf,
        cargo=dto.cargo,
        empresa_id=dto.empresa_id,
        jornada_padrao=dto.jornada_padrao,
        horario_personalizado=dto.horario_personalizado,
        senha_hash=senha_hash
    )
    session.add(colaborador)
    session.commit()
    session.refresh(colaborador)
    return colaborador

def listar_todos(session: Session, empresa_id: UUID):
    """Lista todos os colaboradores, incluindo inativos"""
    return session.query(Colaborador).filter(Colaborador.empresa_id == empresa_id).all()

def listar_todos_ativos(session: Session, empresa_id: UUID):
    """Lista apenas colaboradores ativos"""
    return session.query(Colaborador).filter(
        Colaborador.empresa_id == empresa_id,
        Colaborador.status == Status.ATIVO
    ).all()

def buscar_por_id_e_empresa(session: Session, id: UUID, empresa_id: UUID):
    return session.query(Colaborador).filter(
        Colaborador.id == id,
        Colaborador.empresa_id == empresa_id
    ).first()

def buscar_por_cpf(session: Session, cpf: str):
    return session.query(Colaborador).filter(Colaborador.cpf == cpf).first()

def buscar_por_nome(session: Session, nome: str):
    return session.query(Colaborador).filter(Colaborador.nome.ilike(f"%{nome}%")).all()

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
