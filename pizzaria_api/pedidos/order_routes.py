from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pizzaria_api.dependencies.dependencies import pegar_sessao, verificar_token
from pizzaria_api.schemas.schemas import PedidoSchema
from pizzaria_api.database.models import Pedido, Usuario



order_router = APIRouter(prefix="/orders", tags=["Pedidos"], dependencies=[Depends(verificar_token)])


@order_router.get("/")
async def pedido():
    """Essa é a rota de pedidos, todos os pedidos precisam ser autenticados"""
    return {"message": "Rota de pedidos"}

@order_router.post("/criar_pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(
        usuario_id=pedido_schema.id_usuario
    )
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Pedido criado com sucesso, pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException (status_code=404, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Apenas administradores ou o dono do pedido podem cancelar o pedido")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "message": f"Pedido número: {pedido.id} cancelado com sucesso", "pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Apenas administradores podem listar todos os pedidos")
    else:
        pedidos = session.query(Pedido).all()
        # pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return {"pedidos": pedidos}
