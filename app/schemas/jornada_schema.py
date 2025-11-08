from pydantic import BaseModel, constr
from uuid import UUID
from typing import List, Optional
from datetime import time

# DTO para criar horário (input)
class HorarioJornadaCreateDTO(BaseModel):
    dia_semana: constr(strip_whitespace=True)
    hora_inicio: time
    hora_fim: time

# DTO para atualizar horário (input)
class HorarioJornadaUpdateDTO(BaseModel):
    dia_semana: Optional[constr(strip_whitespace=True)]
    hora_inicio: Optional[time]
    hora_fim: Optional[time]

# DTO para resposta (output)
class HorarioJornadaResponseDTO(BaseModel):
    id: UUID
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
    horarios: List[HorarioJornadaCreateDTO] = []

# DTO para atualização de jornada
class JornadaUpdateDTO(BaseModel):
    nome: Optional[constr(strip_whitespace=True)]
    horas_semanais: Optional[int]
    horarios: Optional[List[HorarioJornadaCreateDTO]]

# DTO de resposta de jornada
class JornadaResponseDTO(BaseModel):
    id: UUID
    nome: str
    horas_semanais: int
    empresa_id: UUID
    horarios: List[HorarioJornadaCreateDTO] = []

    class Config:
        orm_mode = True


# DTO para criar horário (input)
class HorarioJornadaCreateDTO(BaseModel):
    dia_semana: constr(strip_whitespace=True)
    hora_inicio: time
    hora_fim: time

# DTO para atualizar horário (input)
class HorarioJornadaUpdateDTO(BaseModel):
    dia_semana: Optional[constr(strip_whitespace=True)]
    hora_inicio: Optional[time]
    hora_fim: Optional[time]

# DTO para resposta (output)
class HorarioJornadaResponseDTO(BaseModel):
    id: UUID
    dia_semana: constr(strip_whitespace=True)
    hora_inicio: time
    hora_fim: time

    class Config:
        orm_mode = True
