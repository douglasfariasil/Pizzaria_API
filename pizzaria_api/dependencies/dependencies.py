from fastapi import Depends, HTTPException
from pizzaria_api.utils.security import SECRET_KEY, ALGORITHM, oauth2_scheme
from sqlalchemy.orm import sessionmaker, Session
from pizzaria_api.database.models import db, Usuario
from jose import jwt, JWTError


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_scheme), session: Session=Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado, token inválido ou expirado")
    usuario = session.query(Usuario).filter(Usuario.id == usuario).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Acesso inválido ou expirado")
    return usuario
    # --- IGNORE ---    
