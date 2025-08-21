from enum import Enum

class Role(str, Enum):
    SUPER_USER = "super_user"   # você, acesso total
    EMPRESA = "empresa"         # master da empresa
    ADMIN = "admin"             # gerencia colaboradores da empresa
    COLABORADOR = "colaborador" # apenas seus próprios dados
