import uuid
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.roles import Role
from app.status import Status  # importando enum de status

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    # Permissões e status
    role = Column(Enum(Role, native_enum=False), default=Role.EMPRESA, nullable=False)
    status = Column(Enum(Status, native_enum=False), default=Status.ATIVO, nullable=False)

    # Relação com colaboradores
    colaboradores = relationship("Colaborador", back_populates="empresa", cascade="all, delete-orphan")

    # Relação com jornadas
    jornadas = relationship("Jornada", back_populates="empresa", cascade="all, delete-orphan")
