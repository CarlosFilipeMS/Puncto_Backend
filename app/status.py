from enum import Enum as PyEnum
from sqlalchemy import Column, String, Enum, Boolean

class Status(str, PyEnum):
    ATIVO = "ativo"
    INATIVO = "inativo"

# Colaborador
status = Column(Enum(Status, native_enum=False), default=Status.ATIVO, nullable=False)

# Empresa
status = Column(Enum(Status, native_enum=False), default=Status.ATIVO, nullable=False)
