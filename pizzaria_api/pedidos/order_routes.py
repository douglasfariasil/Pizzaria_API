from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["Pedidos"])

@order_router.get("/")
async def pedido():
    """Essa é a rota de pedidos, todos os pedidos precisam ser autenticados"""
    return {"message": "Rota de pedidos"}

