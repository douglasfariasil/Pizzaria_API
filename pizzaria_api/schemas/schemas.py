from pydantic import BaseModel
from typing import Optional, List


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] 
    admin: Optional[bool] 

    class Config:
        from_attributes = True

class PedidoSchema(BaseModel):
    id_usuario: int
    
    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    preco_unitario: float
    tamanho: str
    
    class Config:
        from_attributes = True

# dar informações de pedido a o usuário que fez o pedido
class PedidoInfoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema] = []

    class Config:
        from_attributes = True