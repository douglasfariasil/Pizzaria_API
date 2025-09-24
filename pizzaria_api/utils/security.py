from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form")

# Adicione as variáveis abaixo:
ALGORITHM = "HS256"
SECRET_KEY = "sua_chave_secreta_aqui"  # Troque por uma chave segura!
ACCESS_TOKEN_EXPIRE_MINUTES = 30    