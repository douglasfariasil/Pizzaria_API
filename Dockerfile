# Use uma imagem oficial do Python como base
FROM python:3.11-slim-bookworm

# Evita criação de .pyc e força logs sem buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Diretório de trabalho
WORKDIR /app

# Instala dependências de sistema necessárias para compilar algumas dependências Python
# e ca-certificates para HTTPS
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    cargo \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências Python
COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Remove pacotes de build para reduzir a imagem (opcional)
RUN apt-get remove -y build-essential python3-dev cargo \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia o código da aplicação
COPY . .

# Criar usuário não-root e dar propriedade dos arquivos
RUN addgroup --system app && adduser --system --ingroup app app \
    && chown -R app:app /app

USER app

# Porta exposta
EXPOSE 8000

# Comando padrão para iniciar o app (ajuste se usar gunicorn/uvicorn workers diferentes)
CMD ["uvicorn", "pizzaria_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

# Instruções para execução do contêiner
# docker run --rm -p 8000:8000 pizzaria-api:latest
# docker build -t pizzaria-api:latest .
