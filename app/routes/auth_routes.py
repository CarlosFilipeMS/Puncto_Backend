from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import sessionmaker

from app.models.colaborador import Colaborador
from app.database import engine
from dependencies import pegar_sessao

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "você acesso a rota padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(cpf: str, nome: str, cargo: str, senha_hash, session = Depends(pegar_sessao)):
    Session = sessionmaker(bind=engine)
    session = Session()
    colaborador = session.query(Colaborador).filter(Colaborador.cpf==cpf).first()
    if colaborador:
        return {"mensagem": "E-mail já cadastrado"}
    else:
        novo_colaborador = Colaborador(nome, cpf, cargo ,senha_hash)
        session.add(novo_colaborador)
        session.commit()
        return  {"mensagem": "Colaborador cadastrado com sucesso!"}

