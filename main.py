from fastapi import FastAPI

from pizzaria_api.autenticacao.auth_routes import auth_router
from pizzaria_api.pedidos.order_routes import order_router

app = FastAPI(title="PizzariaAPI")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

app.include_router(auth_router)
app.include_router(order_router)


# para rodar o código no terminal = uvicorn pizzaria_api.main:app --reload
