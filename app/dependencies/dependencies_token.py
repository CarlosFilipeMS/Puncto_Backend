# app/dependencies/dependencies_token.py

from fastapi import Depends
from fastapi import HTTPException
from app.utils.jwt import decode_token  # supondo que você já tenha
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # ou o caminho que estiver usando

def get_empresa_id_from_token(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        payload = decode_token(token)
        empresa_id = payload.get("empresa_id")
        if not empresa_id:
            raise ValueError("empresa_id não encontrado no token")
        return UUID(empresa_id)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido")
