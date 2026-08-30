from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from domain.enums import CanalPedido, StatusPedido, PerfilUsuario

# ==========================================
# SCHEMAS DE USUÁRIO (Para Cadastro e Login)
# ==========================================
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: PerfilUsuario

    class Config:
        from_attributes = True  # Permite ler dados direto do banco de dados (SQLAlchemy)

# ==========================================
# SCHEMAS DE AUTENTICAÇÃO (Token)
# ==========================================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# ==========================================
# SCHEMAS DE PEDIDO (O Fluxo Crítico)
# ==========================================
class PedidoCreate(BaseModel):
    canal_pedido: CanalPedido  # Obriga a enviar "APP", "TOTEM", etc.
    forma_pagamento: str       # Ex: "MOCK", "PIX"
    total: float               # Simplificado para o MVP do projeto

class PedidoResponse(BaseModel):
    id: int
    canal_pedido: CanalPedido
    status: StatusPedido
    total: float
    forma_pagamento: str
    cliente_id: int
    data_criacao: datetime

    class Config:
        from_attributes = True

# ==========================================
# SCHEMA DE ERRO PADRÃO (Exigência do Roteiro)
# ==========================================
class ErroPadrao(BaseModel):
    error: str
    message: str