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
    consentimento_lgpd: bool  # Exigência explícita da LGPD
    perfil: PerfilUsuario = PerfilUsuario.CLIENTE  # Padrão é CLIENTE, mas deixa criar ADMIN

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
class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float

class PedidoCreate(BaseModel):
    canal_pedido: CanalPedido
    forma_pagamento: str
    itens: list[ItemPedidoCreate]

class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float
    class Config:
        from_attributes = True

class PedidoResponse(BaseModel):
    id: int
    canal_pedido: CanalPedido
    status: StatusPedido
    total: float
    forma_pagamento: str
    cliente_id: int
    data_criacao: datetime
    itens: list[ItemPedidoResponse] # Devolve a lista de itens na resposta
    class Config:
        from_attributes = True

# ==========================================
# SCHEMA DE ERRO PADRÃO (Exigência do Roteiro)
# ==========================================
class ErroPadrao(BaseModel):
    error: str
    message: str