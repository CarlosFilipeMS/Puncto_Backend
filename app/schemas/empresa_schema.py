from pydantic import BaseModel, EmailStr, constr
from uuid import UUID

# DTO de criação
class EmpresaCreateDTO(BaseModel):
    nome: constr(strip_whitespace=True, min_length=2)
    cnpj: constr(strip_whitespace=True, min_length=14, max_length=18)  # 14 números, ou com máscara
    email: EmailStr
    senha: constr(min_length=6)

# DTO de resposta (para retornar dados sem expor senha)
class EmpresaResponseDTO(BaseModel):
    id: UUID
    nome: str
    cnpj: str
    email: EmailStr

    class Config:
        orm_mode = True

# DTO para login de empresa
class EmpresaLoginDTO(BaseModel):
    cnpj: str
    senha: str
