from pydantic import BaseModel, constr, Field
from uuid import UUID


class ColaboradorCreateDTO(BaseModel):
    nome: str
    cpf: constr(min_length=11, max_length=11)
    cargo: str
    senha: str
    empresa_id: UUID
    jornada_padrao: int | None = Field(default=None, ge=0, le=168)  # horas por semana
    horario_personalizado: str | None = None


class ColaboradorResponseDTO(BaseModel):
    id: UUID
    nome: str
    cpf: str
    cargo: str
    jornada_padrao: int | None = None
    horario_personalizado: str | None = None
    empresa_id: UUID

    class Config:
        orm_mode = True
