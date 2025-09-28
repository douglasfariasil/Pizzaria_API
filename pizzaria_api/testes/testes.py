import requests

# Login credentials
data = {
    "username": "seu_email",
    "password": "sua_senha"
}

# Perform login
response = requests.post("http://127.0.0.1:8000/auth/login-form", data=data)
print(response.json())

# Uncomment and set your token here to use it for authenticated requests
# token = "SEU_TOKEN_AQUI"
# headers = {
#     "Authorization": f"Bearer {token}"
# }

# Example of creating an order
# data = {
#     "usuario_id": 1,
#     "itens": "Pizza Calabresa",
#     "status": "PENDENTE",
#     "preco": 50.0
# }
# response = requests.post("http://127.0.0.1:8000/orders/criar_pedido", json=data, headers=headers)
# print(response.status_code)
# print(response.json())

# Uncomment to refresh token
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzU5MDk3NDc5fQ.xK2sE33834gonGeQT4bEx0pbrFKAHwPhLaX9qXUCdss"
# }
# requisicao = requests.post("http://127.0.0.1:8000/auth/refresh_token", headers=headers)
# print(requisicao)
# print(requisicao.json())


headers = {
    "Authorization": "Bearer <seu_token_aqui>"
}
requisicao = requests.post("http://127.0.0.1:8000/auth/refresh_token", headers=headers)
