from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

@auth_router.get("/")
async def autentica():
    """
    Essa é a rota de autenticação do sistema
    """
    return {"message": "Você acessou a rota de autenticação", "autenticado": False}

