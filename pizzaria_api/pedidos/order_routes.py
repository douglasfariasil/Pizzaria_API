from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pizzaria_api.dependencies.dependencies import pegar_sessao, verificar_token
from pizzaria_api.schemas.schemas import PedidoSchema, ItemPedidoSchema, PedidoInfoSchema
from pizzaria_api.database.models import Pedido, Usuario, ItemPedido
from typing import List


order_router = APIRouter(prefix="/orders", tags=["Pedidos"], dependencies=[Depends(verificar_token)])


@order_router.get("/")
async def pedido():
    """
    Essa é a rota de pedidos, todos os pedidos precisam ser autenticados
    """
    return {"message": "Rota de pedidos"}

@order_router.post("/criar_pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    """
    Cria um novo pedido para o usuário autenticado
    """
    novo_pedido = Pedido(
        usuario_id=pedido_schema.id_usuario
    )
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Pedido criado com sucesso, pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Para cancela os pedido
    """
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
    """
    Listar todos os pedidos
    """
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Apenas administradores podem listar todos os pedidos")
    else:
        pedidos = session.query(Pedido).all()
        # pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return {
        "pedidos": pedidos
    }

@order_router.post("/pedido/adicionar_item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int,item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), 
    usuario: Usuario = Depends (verificar_token)):
    """
    Adiciona um item ao pedido
    """
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Apenas o dono do pedido ou administradores podem adicionar itens")
    item_pedido = ItemPedido(
        item_pedido_schema.quantidade,
        item_pedido_schema.sabor,
        item_pedido_schema.preco_unitario,
        item_pedido_schema.tamanho,
        id_pedido
    )
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "message": f"Item adicionado ao pedido {pedido.id} com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }
    

@order_router.post("/pedido/remover_item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, session: Session = Depends(pegar_sessao), 
    usuario: Usuario = Depends(verificar_token)):
    """
    Remover um item dos pedido
    """
    item_a_remover = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    if not item_a_remover:
        raise HTTPException(status_code=400, detail="item no pedido não encontrado")
    pedido = item_a_remover.pedido_ref
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Apenas o dono do pedido ou administradores podem remover itens")
    session.delete(item_a_remover)
    pedido.calcular_preco()
    session.commit()
    return {
        "message": "Item removido do pedido com sucesso",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

# Finalizar um pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Finaliza um pedido
    """
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Apenas o dono do pedido ou administradores podem finalizar o pedido")
    if pedido.status != "PENDENTE":
        raise HTTPException(status_code=400, detail="Apenas pedidos com status PENDENTE podem ser finalizados")
    if len(pedido.itens) == 0:
        raise HTTPException(status_code=400, detail="Não é possível finalizar um pedido sem itens")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "message": f"Pedido {pedido.id} finalizado com sucesso",
        "pedido": pedido
    }

# visualizar detalhes de um pedido
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ 
    Visualizar os detalhes de um pedido
    """
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Apenas o dono do pedido ou administradores podem visualizar o pedido")
    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

# visualizar todos os pedidos do usuário logado
@order_router.get("/listar/pedidos_usuario", response_model=List[PedidoInfoSchema])
async def listar_pedidos_usuario(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Listar todos os pedidos do usuário logado
    """
    pedidos = session.query(Pedido).filter(Pedido.usuario_id == usuario.id).all()
    return pedidos
