import os
import sys
import importlib
import pytest

# garantir que o root do projeto esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pizzaria_api.main import app
from pizzaria_api.dependencies.dependencies import pegar_sessao
from pizzaria_api.database.models import Base

# criar engine de teste (SQLite em memória) e manter uma conexão aberta
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
connection = engine.connect()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)

# importar módulos de modelos para registrar as tabelas no Base.metadata
for module_name in (
    "pizzaria_api.autenticacao.models",
    "pizzaria_api.pedidos.models",
    "pizzaria_api.database.models",
):
    try:
        importlib.import_module(module_name)
    except ModuleNotFoundError:
        # ignora se o módulo não existir nesse caminho
        continue

# cria todas as tabelas na conexão compartilhada (mantém o DB em memória)
Base.metadata.create_all(bind=connection)


# dependency override para usar sessão de teste
def _get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[pegar_sessao] = _get_test_db


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
    # teardown: limpar e fechar conexão ao fim da sessão de testes
    Base.metadata.drop_all(bind=connection)
    connection.close()
    engine.dispose()
