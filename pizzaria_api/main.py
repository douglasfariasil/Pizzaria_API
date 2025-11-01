from fastapi import FastAPI
from dotenv import load_dotenv


from pizzaria_api.autenticacao.auth_routes import auth_router
from pizzaria_api.pedidos.order_routes import order_router


load_dotenv()

app = FastAPI()


app.include_router(auth_router)
app.include_router(order_router)


# para rodar o código no terminal = uvicorn pizzaria_api.main:app --reload// a nova uvicorn pizzaria_api.main:app --reload --port 8001
# http://127.0.0.1:8000/docs