from typing import Optional
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
    nome = Column(String(100), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    telefone = Column(String(20), nullable=True)

    def __init__(
        self,
        nome: Optional[str] = None,
        email: Optional[str] = None,
        senha: Optional[str] = None,
        ativo: bool = True,
        admin: bool = False,
        telefone: Optional[str] = None,
    ):
        # aceita posição ou nomeados; atributos None são permitidos se desejado
        if nome is not None:
            self.nome = nome
        if email is not None:
            self.email = email
        if senha is not None:
            self.senha = senha
        self.ativo = ativo
        self.admin = admin
        if telefone is not None:
            self.telefone = telefone

    # relacionamentos
    pedidos = relationship(
        "Pedido",
        back_populates="dono_pedido",
        cascade="all, delete-orphan"
    )


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(50), default="PENDENTE")
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    preco = Column(Float, default=0.0)

    dono_pedido = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", 
    cascade="all, delete", back_populates="pedido_ref")

    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)
        return self.preco

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    sabor = Column(String(100))
    preco_unitario = Column(Float)
    quantidade = Column(Integer)
    tamanho = Column(String(10), default="M")

    pedido_ref = relationship("Pedido", back_populates="itens")
