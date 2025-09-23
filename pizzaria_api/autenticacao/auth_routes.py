from fastapi import APIRouter, Depends, HTTPException
from pizzaria_api.autenticacao.models import Usuario
from pizzaria_api.dependencies.dependencies import pegar_sessao
from pizzaria_api.utils.security import bcrypt_context, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from pizzaria_api.schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])


def criar_token(usuario_id, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_hora_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": usuario_id, "exp": data_hora_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

def verificar_token(token, session: Session=Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == 1).first()
    return usuario

    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     usuario_id = payload.get("sub")
    #     if usuario_id is None:
    #         return None
    #     usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    #     return usuario
    # except JWTError:
    #     return None

def autentica_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get("/")
async def autentica():
    """
    Essa é a rota de autenticação do sistema
    """
    return {"message": "Você acessou a rota de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"message": f"Usuário cadastrado com sucesso: {usuario_schema.email}"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autentica_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=5))  # Token de refresh com duração maior (5 dia)
        return {"access_token": access_token, 
                "refresh_token": refresh_token,
                "token_type": "bearer",
        }
    
    
@auth_router.post("/refresh_token")
async def refresh_token(token):
    usuario = verificar_token(token)
    access_token = criar_token(usuario.id)
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
    }
