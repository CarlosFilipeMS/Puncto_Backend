from pydantic import BaseModel, EmailStr, constr
from uuid import UUID
from app.roles import Role
from app.status import Status

# DTO de criação
class EmpresaCreateDTO(BaseModel):
    nome: constr(strip_whitespace=True, min_length=2)
    cnpj: constr(strip_whitespace=True, min_length=14, max_length=18)
    email: EmailStr
    senha: constr(min_length=6)

# DTO de resposta (sem expor senha)
class EmpresaResponseDTO(BaseModel):
    id: UUID
    nome: str
    cnpj: str
    email: EmailStr
    role: Role
    status: Status

    class Config:
        orm_mode = True

# DTO para login
class EmpresaLoginDTO(BaseModel):
    cnpj: str
    senha: str

# DTO para atualizar status ou role
class EmpresaUpdateStatusRoleDTO(BaseModel):
    status: Status | None = None
    role: Role | None = None
