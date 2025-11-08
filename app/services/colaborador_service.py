from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status

from app.schemas.colaborador_schema import (
    ColaboradorCreateDTO,
    ColaboradorUpdateDTO,
    ColaboradorLoginDTO
)
from app.utils.security import gerar_hash_senha, verificar_senha
from app.utils.jwt import criar_token_jwt
from app.repositories.colaborador_repository import (
    salvar_colaborador,
    listar_todos,
    listar_todos_ativos,
    buscar_por_id_e_empresa,
    buscar_por_cpf_e_empresa,
    buscar_por_nome,
    buscar_por_email_e_empresa,
    atualizar_status_e_role_colaborador
)
from app.roles import Role
from app.models.colaborador import Status

# ----------------- CRUD -----------------
def criar_colaborador_service(dto: ColaboradorCreateDTO, session: Session, empresa_id: UUID):
    if buscar_por_email_e_empresa(session, dto.email, empresa_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
    if buscar_por_cpf_e_empresa(session, dto.cpf, empresa_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado")

    senha_hash = gerar_hash_senha(dto.senha)
    colaborador = salvar_colaborador(dto, senha_hash, session, empresa_id)
    return colaborador  # <- não esqueça de retornar


def listar_todos_colaboradores_service(session: Session, empresa_id: UUID):
    return listar_todos(session, empresa_id)

def listar_colaboradores_ativos_service(session: Session, empresa_id: UUID):
    return listar_todos_ativos(session, empresa_id)

def buscar_por_id_service(session: Session, colaborador_id: UUID, empresa_id: UUID):
    colaborador = buscar_por_id_e_empresa(session, colaborador_id, empresa_id)
    if not colaborador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado")
    return colaborador

def buscar_por_cpf_service(session: Session, cpf: str, empresa_id: UUID):
    colaborador = buscar_por_cpf_e_empresa(session, cpf, empresa_id)
    if not colaborador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado")
    return colaborador

def buscar_por_nome_service(session: Session, nome: str, empresa_id: UUID):
    colaboradores = buscar_por_nome(session, nome, empresa_id)
    if not colaboradores:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum colaborador encontrado com esse nome")
    return colaboradores

def atualizar_colaborador_service(session: Session, colaborador_id: UUID, empresa_id: UUID, dto: ColaboradorUpdateDTO):
    colaborador = buscar_por_id_e_empresa(session, colaborador_id, empresa_id)
    if not colaborador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado")

    if dto.nome:
        colaborador.nome = dto.nome
    if dto.email:
        existente = buscar_por_email_e_empresa(session, dto.email, empresa_id)
        if existente and existente.id != colaborador.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
        colaborador.email = dto.email
    if dto.cargo:
        colaborador.cargo = dto.cargo
    if dto.jornada_id:
        colaborador.jornada_id = dto.jornada_id
    if dto.senha:
        colaborador.senha_hash = gerar_hash_senha(dto.senha)

    session.commit()
    session.refresh(colaborador)
    return colaborador

def atualizar_status_role_colaborador_service(session: Session, colaborador_id: UUID, status: Status | None = None, role: Role | None = None):
    colaborador = atualizar_status_e_role_colaborador(session, colaborador_id, status, role)
    if not colaborador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado")
    return colaborador

# ----------------- LOGIN -----------------
def login_colaborador_service(dto: ColaboradorLoginDTO, session: Session, empresa_id: UUID):
    colaborador = buscar_por_email_e_empresa(session, dto.email, empresa_id)

    if not colaborador or not verificar_senha(dto.senha, colaborador.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if colaborador.status != Status.ATIVO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Colaborador inativo ou bloqueado"
        )

    token = criar_token_jwt(
        subject=str(colaborador.id),
        additional_claims={
            "empresa_id": str(colaborador.empresa_id),
            "role": colaborador.role.value
        }
    )

    return {"access_token": token, "token_type": "bearer"}
