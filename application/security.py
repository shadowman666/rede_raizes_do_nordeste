import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt

# Configurações do Token JWT
SECRET_KEY = "chave_secreta_provisoria_do_projeto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def gerar_hash_senha(senha: str) -> str:
    """Recebo a senha limpa, converto para bytes e devolvo o hash seguro com bcrypt."""
    senha_bytes = senha.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha_bytes, salt).decode("utf-8")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifico se a senha enviada confere com o hash armazenado."""
    senha_bytes = senha_plana.encode("utf-8")[:72]
    hash_bytes = senha_hash.encode("utf-8")
    return bcrypt.checkpw(senha_bytes, hash_bytes)


def criar_token_acesso(dados: dict) -> str:
    """Gero o token de autenticação JWT com prazo de expiração."""
    copia_dados = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    copia_dados.update({"exp": expiracao})

    return jwt.encode(copia_dados, SECRET_KEY, algorithm=ALGORITHM)