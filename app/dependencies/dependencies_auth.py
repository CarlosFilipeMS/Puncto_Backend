from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.dependencies.dependencies_sessao import pegar_sessao
from app.utils.jwt import decode_token
from app.repositories.colaborador_repository import buscar_por_id_e_empresa

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/colaborador/login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    try:
        payload = decode_token(token)
        colaborador_id: str = payload.get("sub")
        empresa_id: str = payload.get("empresa_id")

        if not colaborador_id or not empresa_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        colaborador = buscar_por_id_e_empresa(session, colaborador_id, empresa_id)
        if not colaborador:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return colaborador

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
