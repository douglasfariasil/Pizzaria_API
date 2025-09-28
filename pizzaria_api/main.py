from fastapi import FastAPI
from dotenv import load_dotenv
import os

from pizzaria_api.autenticacao.auth_routes import auth_router
from pizzaria_api.pedidos.order_routes import order_router
from pizzaria_api.utils.security import bcrypt_context


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()



app.include_router(auth_router)
app.include_router(order_router)


# para rodar o código no terminal = uvicorn pizzaria_api.main:app --reload
# http://127.0.0.1:8000/docs