from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt, JWTError
from typing import Union
from uuid import UUID
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRA_MINUTOS = int(os.getenv("EXPIRA_MINUTOS", 60 * 24))

if not SECRET_KEY:
    raise ValueError("SECRET_KEY não definida no .env")

def criar_token_jwt(empresa_id: Union[UUID, str]):
    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRA_MINUTOS)
    payload = {
        "sub": str(empresa_id),
        "empresa_id": str(empresa_id),
        "exp": expiracao
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
