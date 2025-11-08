from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Union
from uuid import UUID
import os
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# Configurações do JWT
# =====================================================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRA_MINUTOS = int(os.getenv("EXPIRA_MINUTOS", 60 * 24))  # 24h por padrão

if not SECRET_KEY:
    raise ValueError("SECRET_KEY não definida no .env")

# Rota padrão do OAuth2 — usada em Depends
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# =====================================================
# Criar Token JWT
# =====================================================
def criar_token_jwt(subject: Union[UUID, str], additional_claims: dict = None) -> str:
    """
    Cria um token JWT com o ID (subject) e claims adicionais opcionais.
    """
    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRA_MINUTOS)
    payload = {
        "sub": str(subject),
        "exp": expiracao
    }
    if additional_claims:
        payload.update(additional_claims)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# =====================================================
# Decodificar Token JWT
# =====================================================
def decode_token(token: str) -> dict:
    """
    Decodifica um token JWT e retorna o payload (claims).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


# =====================================================
# Obter ID da empresa do token (para rotas autenticadas)
# =====================================================
def get_empresa_id_from_token(token: str = Depends(oauth2_scheme)) -> UUID:
    """
    Extrai o campo 'empresa_id' do token JWT e o retorna como UUID.
    Lança 401 se o token for inválido.
    """
    payload = decode_token(token)
    empresa_id = payload.get("empresa_id")

    if not empresa_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não contém empresa_id",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return UUID(empresa_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="empresa_id inválido no token",
            headers={"WWW-Authenticate": "Bearer"},
        )
