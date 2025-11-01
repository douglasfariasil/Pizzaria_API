from fastapi.testclient import TestClient


def test_criar_conta_sucesso(client: TestClient):
    """
    Testa a criação de uma nova conta com sucesso.
    Verifica se o status code é 200 e se a mensagem de resposta está correta.
    """
    response = client.post(
        "/auth/criar_conta",
        json={"nome": "Teste User", "email": "teste@example.com", "senha": "testpassword", "ativo": True, "admin": False},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Usuário cadastrado com sucesso: teste@example.com"}


def test_criar_conta_email_duplicado(client: TestClient):
    """
    Testa a tentativa de criar uma conta com um e-mail que já existe.
    Verifica se o status code é 400 e se a mensagem de detalhe do erro está correta.
    """
    # Primeiro, cria um usuário para garantir que o e-mail exista no banco
    client.post(
        "/auth/criar_conta",
        json={"nome": "Teste User", "email": "duplicado@example.com", "senha": "testpassword", "ativo": True, "admin": False},
    )

    # Agora, tenta criar outro usuário com o mesmo e-mail
    response = client.post(
        "/auth/criar_conta",
        json={"nome": "Outro User", "email": "duplicado@example.com", "senha": "anotherpassword", "ativo": True, "admin": False},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "E-mail do usuário já cadastrado"}
    