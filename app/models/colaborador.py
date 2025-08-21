import uuid
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.roles import Role
from app.status import Status  # ✅ importando o enum de status

class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    cargo = Column(String, nullable=False)
    jornada_padrao = Column(String, nullable=True)  # Horas por semana
    horario_personalizado = Column(String, nullable=True)
    senha_hash = Column(String, nullable=True)

    # Permissões e status
    role = Column(Enum(Role, native_enum=False), default=Role.COLABORADOR, nullable=False)
    status = Column(Enum(Status, native_enum=False), default=Status.ATIVO, nullable=False)

    # Relação com a empresa
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"), nullable=False)
    empresa = relationship("Empresa", back_populates="colaboradores")
