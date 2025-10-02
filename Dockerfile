# Use uma imagem oficial do Python como imagem base
FROM python:3.11-slim-bullseye

# Atualiza os pacotes do sistema para corrigir vulnerabilidades conhecidas
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
# Usamos pymysql para conectar ao MySQL
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta 8000 para o mundo fora deste contêiner
EXPOSE 8000

# Define a variável de ambiente PYTHONPATH para que os imports funcionem
ENV PYTHONPATH=/app

# Comando para executar a aplicação quando o contêiner iniciar
CMD ["uvicorn", "pizzaria_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
