from sqlalchemy.orm import Session
from uuid import UUID
from app.models.empresa import Empresa, Status
from app.schemas.empresa_schema import EmpresaCreateDTO

def salvar_empresa(dto: EmpresaCreateDTO, senha_hash: str, session: Session) -> Empresa:
    empresa = Empresa(
        nome=dto.nome,
        cnpj=dto.cnpj,
        email=dto.email,
        senha_hash=senha_hash
    )
    session.add(empresa)
    session.commit()
    session.refresh(empresa)
    return empresa

def listar_todas_empresas(session: Session):
    """Lista todas as empresas, incluindo inativas"""
    return session.query(Empresa).all()

def listar_todas_empresas_ativas(session: Session):
    """Lista apenas empresas ativas"""
    return session.query(Empresa).filter(Empresa.status == Status.ATIVO).all()

def buscar_por_id(session: Session, empresa_id: UUID):
    return session.query(Empresa).filter(Empresa.id == empresa_id).first()

def buscar_por_email(session: Session, email: str):
    return session.query(Empresa).filter(Empresa.email == email).first()

def buscar_por_cnpj(session: Session, cnpj: str):
    return session.query(Empresa).filter(Empresa.cnpj == cnpj).first()

def deletar_empresa(session: Session, empresa_id: UUID) -> bool:
    empresa = buscar_por_id(session, empresa_id)
    if not empresa:
        return False
    session.delete(empresa)
    session.commit()
    return True

def atualizar_empresa(session: Session, empresa_id: UUID, dto: EmpresaCreateDTO, senha_hash: str | None = None):
    empresa = session.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        return None

    empresa.nome = dto.nome
    empresa.cnpj = dto.cnpj
    empresa.email = dto.email
    if senha_hash:
        empresa.senha_hash = senha_hash

    session.commit()
    session.refresh(empresa)
    return empresa

def atualizar_status(
    session: Session,
    empresa_id: UUID,
    status: Status
):
    empresa = session.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        return None

    empresa.status = status
    session.commit()
    session.refresh(empresa)
    return empresa
