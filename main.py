from fastapi import FastAPI


app = FastAPI()

# Importar o nome do projeto.pasta.arquivo por fim um nome qualquer
from pizzaria_api.auteticacao.auth_routes import auth_router
from pizzaria_api.pedidos.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)





# para rodar o código no terminal = uvicorn main:app --reload
