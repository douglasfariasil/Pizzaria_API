from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Adicione as variáveis abaixo:
ALGORITHM = "HS256"
SECRET_KEY = "sua_chave_secreta_aqui"  # Troque por uma chave segura!
ACCESS_TOKEN_EXPIRE_MINUTES = 30    