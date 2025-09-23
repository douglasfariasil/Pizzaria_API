from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pizzaria_api.dependencies.dependencies import pegar_sessao
from pizzaria_api.schemas import PedidoSchema
from pizzaria_api.autenticacao.models import Pedido

order_router = APIRouter(prefix="/orders", tags=["Pedidos"])

@order_router.get("/")
async def pedido():
    """Essa é a rota de pedidos, todos os pedidos precisam ser autenticados"""
    return {"message": "Rota de pedidos"}

@order_router.post("/criar_pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(
        usuario_id=pedido_schema.usuario_id,
        itens=pedido_schema.itens,
        # status="PENDENTE",
        # preco=pedido_schema.preco
    )
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Pedido criado com sucesso, pedido_id: {novo_pedido.id}"}
