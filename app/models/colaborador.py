# app/models/colaborador_model.py
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    cargo = Column(String, nullable=False)
    jornada_padrao = Column(String, nullable=True)
    horario_personalizado = Column(String, nullable=True)
    senha_hash = Column(String, nullable=True)

    #empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"))

    # IMPLEMENTAR QUANDO TIVER AS OUTRAS TABLEAS
    # empresa = relationship("Empresa", back_populates="colaboradores")
    # registros = relationship("RegistroPonto", back_populates="colaborador", cascade="all, delete-orphan")

    def __init__(self,
                 nome,
                 cpf,
                 cargo,
                 #empresa_id,
                 #jornada_padrao,
                 #horario_personalizado,
                 senha_hash):
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo
        #self.empresa_id = empresa_id
        #self.jornada_padrao = jornada_padrao
        #self.horario_personalizado = horario_personalizado
        self.senha_hash = senha_hash

