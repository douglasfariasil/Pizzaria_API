from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from pizzaria_api.database.database import SessionLocal
from pizzaria_api.database.models import Usuario
from pizzaria_api.utils.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-form")

def pegar_sessao():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    db.close() 

def verificar_token(token: str = Depends(
        oauth2_scheme), session: Session = Depends(pegar_sessao)
    ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        usuario = session.query(Usuario).filter(Usuario.id == int(user_id)).first()
        if usuario is None:
            raise credentials_exception
        return usuario
    except JWTError:
        raise credentials_exception

