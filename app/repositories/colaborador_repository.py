from sqlalchemy.orm import Session
from uuid import UUID

from app.models.colaborador import Colaborador
from app.schemas.colaborador_schema import ColaboradorCreateDTO

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
    return session.query(Colaborador).filter(Colaborador.empresa_id == empresa_id).all()

def buscar_por_id_e_empresa(session: Session, id: UUID, empresa_id: UUID):
    return session.query(Colaborador).filter(
        Colaborador.id == id,
        Colaborador.empresa_id == empresa_id
    ).first()


def buscar_por_cpf(session: Session, cpf: str):
    return session.query(Colaborador).filter(Colaborador.cpf == cpf).first()

def buscar_por_nome(session: Session, nome: str):
    return session.query(Colaborador).filter(Colaborador.nome.ilike(f"%{nome}%")).all()
