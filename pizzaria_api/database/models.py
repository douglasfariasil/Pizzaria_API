from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship

# Base para os modelos do SQLAlchemy
Base = declarative_base()


# Criar as classe, tabelas no banco de dados
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    telefone = Column(String, nullable=True)

    pedidos = relationship("Pedido", back_populates="dono_pedido")

    def __init__(
        self,
        nome: str,
        email: str,
        senha: str,
        ativo: bool = True,
        admin: bool = False,
        telefone: str = None,
    ):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
        self.telefone = telefone


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="PENDENTE")
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    preco = Column(Float, default=0.0)

    dono_pedido = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", 
    cascade="all, delete", back_populates="pedido_ref")

    def __init__(self, usuario_id: int, status="PENDENTE", preco=0.0):
        self.usuario_id = usuario_id
        self.status = status
        self.preco = preco

    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)
        return self.preco

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    sabor = Column(String)
    preco_unitario = Column(Float)
    quantidade = Column(Integer)
    tamanho = Column(String, default="M")

    pedido_ref = relationship("Pedido", back_populates="itens")

    def __init__(self, quantidade, sabor, preco_unitario, tamanho, pedido_id):
        self.quantidade = quantidade
        self.sabor = sabor
        self.preco_unitario = preco_unitario
        self.tamanho = tamanho
        self.pedido_id = pedido_id
