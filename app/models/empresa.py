import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    def __init__(self, nome: str, cnpj: str, email: str, senha_hash: str):
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.senha_hash = senha_hash

    colaboradores = relationship("Colaborador", back_populates="empresa", cascade="all, delete-orphan")