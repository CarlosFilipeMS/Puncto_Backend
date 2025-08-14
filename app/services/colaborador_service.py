from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from app.schemas.colaborador_schema import ColaboradorCreateDTO
from app.utils.security import gerar_hash_senha

from app.repositories.colaborador_repository import (
    salvar_colaborador,
    buscar_por_id_e_empresa,
    buscar_por_cpf,
    buscar_por_nome,
    listar_todos
)



def criar_colaborador_service(dto: ColaboradorCreateDTO, session: Session):
    senha_hash = gerar_hash_senha(dto.senha)
    return salvar_colaborador(dto, senha_hash, session)


def listar_todos_colaboradores_service(session: Session, empresa_id: UUID):
    return listar_todos(session, empresa_id)

def buscar_por_id_service(session: Session, id: UUID, empresa_id: UUID):
    colaborador = buscar_por_id_e_empresa(session, id, empresa_id)
    if not colaborador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado")
    return colaborador

def buscar_por_cpf_service(session: Session, cpf: str):
    colaborador = buscar_por_cpf(session, cpf)
    if not colaborador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador não encontrado")
    return colaborador

def buscar_por_nome_service(session: Session, nome: str):
    colaboradores = buscar_por_nome(session, nome)
    if not colaboradores:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum colaborador encontrado com esse nome")
    return colaboradores
