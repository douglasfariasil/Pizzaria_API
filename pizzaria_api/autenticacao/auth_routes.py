from fastapi import APIRouter, Depends, HTTPException
from pizzaria_api.autenticacao.models import Usuario
from pizzaria_api.dependencies.dependencies import pegar_sessao
from pizzaria_api.utils.security import bcrypt_context
from pizzaria_api.schemas import UsuarioSchema
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

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
