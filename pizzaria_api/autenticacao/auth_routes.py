from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

@auth_router.get("/")
async def autentica():
    return {"message": "Você acessou a rota de autenticação", "autenticado": False}

