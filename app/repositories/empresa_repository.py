from sqlalchemy.orm import Session
from uuid import UUID
from app.models.empresa import Empresa
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
    return session.query(Empresa).all()

def buscar_por_id(session: Session, id: UUID):
    return session.query(Empresa).filter(Empresa.id == id).first()

def buscar_por_email(session: Session, email: str):
    return session.query(Empresa).filter(Empresa.email == email).first()

def buscar_por_cnpj(session: Session, cnpj: str):
    return session.query(Empresa).filter(Empresa.cnpj == cnpj).first()

def deletar_empresa(session: Session, id: UUID) -> bool:
    empresa = buscar_por_id(session, id)
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

