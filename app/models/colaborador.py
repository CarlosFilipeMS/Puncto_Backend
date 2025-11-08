import uuid
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from app.database import Base
from app.roles import Role
from app.status import Status


class Colaborador(Base):
    __tablename__ = "colaboradores"
    __table_args__ = (
        UniqueConstraint("cpf", "empresa_id", name="uq_colaborador_cpf_empresa"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)  # email único no sistema
    cpf = Column(String, index=True, nullable=False)  # não é mais unique global
    cargo = Column(String, nullable=False)
    senha_hash = Column(String, nullable=True)

    # Permissões e status
    role = Column(Enum(Role, native_enum=False), default=Role.COLABORADOR, nullable=False)
    status = Column(Enum(Status, native_enum=False), default=Status.ATIVO, nullable=False)

    # Relação com a empresa
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"), nullable=False)
    empresa = relationship("Empresa", back_populates="colaboradores")

    # Relação com jornada
    jornada_id = Column(UUID(as_uuid=True), ForeignKey("jornadas.id"), nullable=True)
    jornada = relationship("Jornada", back_populates="colaboradores")
