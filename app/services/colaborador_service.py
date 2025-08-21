from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from app.schemas.colaborador_schema import ColaboradorCreateDTO
from app.utils.security import gerar_hash_senha
from app.repositories.colaborador_repository import (
    salvar_colaborador,
    listar_todos,
    listar_todos_ativos,
    buscar_por_id_e_empresa,
    buscar_por_cpf,
    buscar_por_nome,
    atualizar_status_e_role_colaborador
)
from app.roles import Role
from app.models.colaborador import Status

# Criar colaborador
def criar_colaborador_service(dto: ColaboradorCreateDTO, session: Session):
    senha_hash = gerar_hash_senha(dto.senha)
    return salvar_colaborador(dto, senha_hash, session)

# Listar todos colaboradores (mesmo inativos)
def listar_todos_colaboradores_service(session: Session, empresa_id: UUID):
    return listar_todos(session, empresa_id)

# Listar apenas colaboradores ativos
def listar_colaboradores_ativos_service(session: Session, empresa_id: UUID):
    return listar_todos_ativos(session, empresa_id)

# Buscar por ID e empresa
def buscar_por_id_service(session: Session, id: UUID, empresa_id: UUID):
    colaborador = buscar_por_id_e_empresa(session, id, empresa_id)
    if not colaborador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado")
    return colaborador

# Buscar por CPF
def buscar_por_cpf_service(session: Session, cpf: str):
    colaborador = buscar_por_cpf(session, cpf)
    if not colaborador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado")
    return colaborador

# Buscar por nome
def buscar_por_nome_service(session: Session, nome: str):
    colaboradores = buscar_por_nome(session, nome)
    if not colaboradores:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum colaborador encontrado com esse nome")
    return colaboradores

# Atualizar dados do colaborador (exceto status e role)
def atualizar_colaborador_service(session: Session, colaborador_id: UUID, dto: ColaboradorCreateDTO, atualizar_senha: bool = False):
    colaborador = buscar_por_id_e_empresa(session, colaborador_id, dto.empresa_id)
    if not colaborador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado")

    if atualizar_senha:
        senha_hash = gerar_hash_senha(dto.senha)
    else:
        senha_hash = None

    # Atualiza campos básicos
    colaborador.nome = dto.nome
    colaborador.cargo = dto.cargo
    colaborador.jornada_padrao = dto.jornada_padrao
    colaborador.horario_personalizado = dto.horario_personalizado
    if senha_hash:
        colaborador.senha_hash = senha_hash

    session.commit()
    session.refresh(colaborador)
    return colaborador

# Atualizar status ou role do colaborador
def atualizar_status_role_colaborador_service(session: Session, colaborador_id: UUID, status: Status | None = None, role: Role | None = None):
    colaborador = atualizar_status_e_role_colaborador(session, colaborador_id, status, role)
    if not colaborador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado")
    return colaborador
