from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["Pedidos"])

@order_router.get("/")
async def pedido():
    return {"message": "Rota de pedidos"}

