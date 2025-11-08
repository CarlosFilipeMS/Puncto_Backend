import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Jornada(Base):
    __tablename__ = "jornadas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String, nullable=False)  # Ex: "Jornada Padrão 40h", "Turno Flexível"
    horas_semanais = Column(Integer, nullable=False)  # Total de horas por semana
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"), nullable=False)

    # Relacionamentos
    empresa = relationship("Empresa", back_populates="jornadas")
    horarios = relationship("HorarioJornada", back_populates="jornada", cascade="all, delete-orphan")
    colaboradores = relationship(
        "Colaborador",
        back_populates="jornada",
        cascade="all, delete-orphan"
    )

class HorarioJornada(Base):
    __tablename__ = "horarios_jornada"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dia_semana = Column(String, nullable=False)  # "Segunda", "Terça", ...
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    jornada_id = Column(UUID(as_uuid=True), ForeignKey("jornadas.id"), nullable=False)

    jornada = relationship("Jornada", back_populates="horarios")
