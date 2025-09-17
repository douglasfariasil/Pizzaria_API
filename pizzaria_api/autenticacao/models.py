from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base


# Configuração da conexão do banco de dados SQLite
db = create_engine("sqlite:///pizzaria_api/database/banco.db")

# Base para os modelos do SQLAlchemy
Base = declarative_base()

# Criar as classe, tabelas no banco de dados
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, index=True)
    email = Column("email", String, unique=True, index=True)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)
    telefone = Column("telefone", String, nullable=True)

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

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = Column("itens", String)

    def __init__(self, usuario_id, itens, status="PENDENTE", preco=0):
        self.usuario_id = usuario_id
        self.status = status
        self.preco = preco
        self.itens = itens


# Itens do pedido
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    pedido_id = Column("pedido_id", Integer, ForeignKey("pedidos.id"))
    sabor = Column("sabor", String)
    preco_unitario = Column("preco_unitario", Float)
    quantidade = Column("quantidade", Integer)
    tamanho = Column("tamanho", String)

    def __init__(self, pedido_id, sabor, preco_unitario, quantidade, tamanho="M"):
        self.pedido_id = pedido_id
        self.sabor = sabor
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade
        self.tamanho = tamanho


# Criar uma sessão para interagir com o banco de dados


# alembic revise --autogenerate -m "Initial migration"