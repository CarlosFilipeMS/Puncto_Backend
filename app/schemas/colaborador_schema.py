from pydantic import BaseModel, constr, Field
from uuid import UUID
from app.roles import Role
from app.status import Status

# DTO de criação
class ColaboradorCreateDTO(BaseModel):
    nome: str
    cpf: constr(min_length=11, max_length=11)
    cargo: str
    senha: str
    empresa_id: UUID
    jornada_padrao: int | None = Field(default=None, ge=0, le=168)
    horario_personalizado: str | None = None

# DTO de resposta
class ColaboradorResponseDTO(BaseModel):
    id: UUID
    nome: str
    cpf: str
    cargo: str
    jornada_padrao: int | None = None
    horario_personalizado: str | None = None
    empresa_id: UUID
    role: Role
    status: Status

    class Config:
        orm_mode = True

# DTO para atualizar status ou role
class ColaboradorUpdateStatusRoleDTO(BaseModel):
    status: Status | None = None
    role: Role | None = None
