import requests

data = {
    "username": "seu_email",
    "password": "sua_senha"
}
response = requests.post("http://127.0.0.1:8000/auth/login-form", data=data)
print(response.json())

# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzU5MDk3NDc5fQ.xK2sE33834gonGeQT4bEx0pbrFKAHwPhLaX9qXUCdss"
# }

# requisicao = requests.post("http://127.0.0.1:8000/auth/refresh_token", headers=headers)
# print(requisicao)
# print(requisicao.json())


# headers = {
#     "Authorization": "Bearer <seu_token_aqui>"
# }
# requisicao = requests.post("http://127.0.0.1:8000/auth/refresh_token", headers=headers)
