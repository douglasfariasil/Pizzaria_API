# Pizzaria API

API em FastAPI para gerenciar autenticação e pedidos de uma pizzaria.

Visão geral

- Backend RESTful usando FastAPI, SQLAlchemy e JWT (python-jose).
- Estrutura modular: autenticação, pedidos, dependências e utilitários.
- Testes com pytest; DB de teste usa SQLite em memória.
- Migrations com Alembic (opcional).

Requisitos

- Python 3.11+
- virtualenv/venv
- SQLite (padrão) ou servidor MySQL/Postgres conforme sua DATABASE_URL
- Opcional: Docker para containerização

Instalação (local)

1. Clone o repositório e entre na pasta:

   ```bash
   git clone <repo-url> .
   cd /home/douglas/pizzaria_api
   ```

2. Crie e ative um virtualenv:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Instale dependências:
   - Se houver `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```
   - Ou use o `pyproject.toml`:
     ```bash
     pip install -U pip setuptools
     pip install -e .
     ```

Variáveis de ambiente (exemplos)

- `.env` recomendado. Variáveis usadas pelo projeto:
  - SECRET_KEY="sua_chave_secreta"
  - ACCESS_TOKEN_EXPIRE_MINUTES=30
  - DATABASE_URL="sqlite:///./db.sqlite3" (padrão para desenvolvimento)
  - OUTRAS variáveis conforme sua configuração

Rodando a aplicação localmente

```bash
# dentro do venv
uvicorn pizzaria_api.main:app --reload --port 8000
# Acesse documentação interativa:
# http://127.0.0.1:8000/docs
```

Rodando testes

```bash
pytest -q
```

- Os testes usam um banco SQLite em memória. Se houver falhas relacionadas a tabelas, verifique `tests/conftest.py` para imports dos modelos e override da dependência de sessão.

Migrations (Alembic)

- Gerar migration:
  ```bash
  alembic revision --autogenerate -m "mensagem"
  ```
- Aplicar migrations:
  ```bash
  alembic upgrade head
  ```

Docker

- Build da imagem:
  ```bash
  docker build -t pizzaria-api:latest .
  ```
- Rodar container:
  ```bash
  docker run --rm -p 8000:8000 pizzaria-api:latest
  ```

Estrutura do projeto (resumo)

- pizzaria_api/
  - main.py — instancia FastAPI e registra routers
  - autenticacao/ — rotas, modelos e lógica de autenticação
  - pedidos/ — rotas e modelos de pedidos
  - database/models.py — modelos SQLAlchemy (Base central)
  - dependencies/ — dependências do FastAPI (pegar_sessao, verificar_token)
  - utils/ — helpers (security, hashing, tokens)
- tests/ — testes com pytest
- alembic/ — migrations (se configurado)
- Dockerfile, pyproject.toml, requirements.txt, README.md

Boas práticas e observações

- Mantenha apenas uma instância de `Base = declarative_base()` e importe-a em todos os modelos.
- Use variáveis de ambiente para SECRET_KEY e DATABASE_URL em produção.
- Remova `__init__` customizados nos modelos salvo se necessário; deixar SQLAlchemy gerenciar inicialização pode evitar erros de mapeamento.
- Ao criar testes com SQLite em memória, mantenha uma conexão compartilhada para evitar perda de estado entre threads.

Contribuição

- Abra issues para bugs/funcionalidades.
- Crie PRs com mudanças pequenas e testes.

Se quiser, eu gero um README mais detalhado com exemplos de requests (curl/httpie) e documentação das rotas.// filepath: /home/douglas/pizzaria_api/README.md

# Pizzaria API

API em FastAPI para gerenciar autenticação e pedidos de uma pizzaria.

Visão geral

- Backend RESTful usando FastAPI, SQLAlchemy e JWT (python-jose).
- Estrutura modular: autenticação, pedidos, dependências e utilitários.
- Testes com pytest; DB de teste usa SQLite em memória.
- Migrations com Alembic (opcional).

Requisitos

- Python 3.11+
- virtualenv/venv
- SQLite (padrão) ou servidor MySQL/Postgres conforme sua DATABASE_URL
- Opcional: Docker para containerização

Instalação (local)

1. Clone o repositório e entre na pasta:

   ```bash
   git clone <repo-url> .
   cd /home/douglas/pizzaria_api
   ```

2. Crie e ative um virtualenv:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Instale dependências:
   - Se houver `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```
   - Ou use o `pyproject.toml`:
     ```bash
     pip install -U pip setuptools
     pip install -e .
     ```

Variáveis de ambiente (exemplos)

- `.env` recomendado. Variáveis usadas pelo projeto:
  - SECRET_KEY="sua_chave_secreta"
  - ACCESS_TOKEN_EXPIRE_MINUTES=30
  - DATABASE_URL="sqlite:///./db.sqlite3" (padrão para desenvolvimento)
  - OUTRAS variáveis conforme sua configuração

Rodando a aplicação localmente

```bash
# dentro do venv
uvicorn pizzaria_api.main:app --reload --port 8000
# Acesse documentação interativa:
# http://127.0.0.1:8000/docs
```

Rodando testes

```bash
pytest -q
```

- Os testes usam um banco SQLite em memória. Se houver falhas relacionadas a tabelas, verifique `tests/conftest.py` para imports dos modelos e override da dependência de sessão.

Migrations (Alembic)

- Gerar migration:
  ```bash
  alembic revision --autogenerate -m "mensagem"
  ```
- Aplicar migrations:
  ```bash
  alembic upgrade head
  ```

Docker

- Build da imagem:
  ```bash
  docker build -t pizzaria-api:latest .
  ```
- Rodar container:
  ```bash
  docker run --rm -p 8000:8000 pizzaria-api:latest
  ```

Estrutura do projeto (resumo)

- pizzaria_api/
  - main.py — instancia FastAPI e registra routers
  - autenticacao/ — rotas, modelos e lógica de autenticação
  - pedidos/ — rotas e modelos de pedidos
  - database/models.py — modelos SQLAlchemy (Base central)
  - dependencies/ — dependências do FastAPI (pegar_sessao, verificar_token)
  - utils/ — helpers (security, hashing, tokens)
- tests/ — testes com pytest
- alembic/ — migrations (se configurado)
- Dockerfile, pyproject.toml, requirements.txt, README.md

Boas práticas e observações

- Mantenha apenas uma instância de `Base = declarative_base()` e importe-a em todos os modelos.
- Use variáveis de ambiente para SECRET_KEY e DATABASE_URL em produção.
- Remova `__init__` customizados nos modelos salvo se necessário; deixar SQLAlchemy gerenciar inicialização pode evitar erros de mapeamento.
- Ao criar testes com SQLite em memória, mantenha uma conexão compartilhada para evitar perda de estado entre threads.

Contribuição

- Abra issues para bugs/funcionalidades.
- Crie PRs com mudanças pequenas e testes.

Se quiser, eu gero um README mais detalhado com exemplos de requests (curl/httpie) e documentação das rotas.
