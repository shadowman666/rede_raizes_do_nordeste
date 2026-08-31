from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from infrastructure.database import get_db
from domain.models import Usuario
from domain.enums import PerfilUsuario
from application.security import SECRET_KEY, ALGORITHM

# Rota onde o cliente obtém o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obter_usuario_logado(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """Valido o token JWT enviado no cabeçalho e retorno o usuário autenticado."""
    erro_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "error": "NAO_AUTORIZADO",
            "message": "Credenciais inválidas ou token expirado",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if not email or not isinstance(email, str):
            raise erro_credenciais
    except JWTError:
        raise erro_credenciais

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise erro_credenciais

    return usuario

# ==========================================
# ROTA GERENCIAL - RBAC
# ==========================================
def obter_usuario_admin(usuario: Usuario = Depends(obter_usuario_logado)):
    if usuario.perfil != PerfilUsuario.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "ACESSO_NEGADO", "message": "Requer privilégios de administrador."}
        )
    return usuario