from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.dependencies_sessao import pegar_sessao
from app.dependencies.dependencies_auth import get_current_user
from app.schemas.colaborador_schema import ColaboradorLoginDTO
from app.services.colaborador_service import login_colaborador_service

auth_colaborador_router = APIRouter(
    prefix="/auth/colaborador",
    tags=["Auth Colaborador"]
)

# ------------------ LOGIN ------------------
@auth_colaborador_router.post("/login")
def login_colaborador(dto: ColaboradorLoginDTO, session: Session = Depends(pegar_sessao)):
    """
    Endpoint para login de colaborador.
    Chama o service que valida usuário, senha e retorna JWT.
    """
    return login_colaborador_service(dto, session)


# ------------------ ROTA PROTEGIDA DE EXEMPLO ------------------
@auth_colaborador_router.get("/me")
def rota_protegida(current_user=Depends(get_current_user)):
    """
    Exemplo de rota protegida.
    Retorna os dados do colaborador autenticado.
    """
    return {
        "id": str(current_user.id),
        "nome": current_user.nome,
        "email": current_user.email,
        "cargo": current_user.cargo,
        "role": current_user.role.value,
        "status": current_user.status.value
    }
