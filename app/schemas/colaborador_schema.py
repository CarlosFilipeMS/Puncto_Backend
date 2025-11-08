from pydantic import BaseModel, constr, EmailStr
from uuid import UUID
from app.roles import Role
from app.status import Status

class ColaboradorCreateDTO(BaseModel):
    nome: str
    email: EmailStr
    cpf: constr(min_length=11, max_length=11)
    cargo: str
    senha: str
    jornada_id: UUID | None = None

class ColaboradorUpdateDTO(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    cargo: str | None = None
    jornada_id: UUID | None = None
    senha: str | None = None

class ColaboradorUpdateStatusRoleDTO(BaseModel):
    status: Status | None = None
    role: Role | None = None

class ColaboradorLoginDTO(BaseModel):
    email: EmailStr
    senha: str

class ColaboradorResponseDTO(BaseModel):
    id: UUID
    nome: str
    email: EmailStr
    cpf: str
    cargo: str
    empresa_id: UUID
    jornada_id: UUID | None = None
    role: Role
    status: Status

    class Config:
        orm_mode = True
