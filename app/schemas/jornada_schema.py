from pydantic import BaseModel, constr
from uuid import UUID
from typing import List, Optional
from datetime import time

# DTO para horário de jornada
class HorarioJornadaDTO(BaseModel):
    id: Optional[UUID]
    dia_semana: constr(strip_whitespace=True)
    hora_inicio: time
    hora_fim: time

    class Config:
        orm_mode = True

# DTO para criação de jornada
class JornadaCreateDTO(BaseModel):
    nome: constr(strip_whitespace=True)
    horas_semanais: int
    empresa_id: UUID
    horarios: List[HorarioJornadaDTO] = []

# DTO para atualização de jornada
class JornadaUpdateDTO(BaseModel):
    nome: Optional[constr(strip_whitespace=True)]
    horas_semanais: Optional[int]
    horarios: Optional[List[HorarioJornadaDTO]]

# DTO de resposta de jornada
class JornadaResponseDTO(BaseModel):
    id: UUID
    nome: str
    horas_semanais: int
    empresa_id: UUID
    horarios: List[HorarioJornadaDTO] = []

    class Config:
        orm_mode = True
