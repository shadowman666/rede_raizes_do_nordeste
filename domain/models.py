from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from infrastructure.database import Base
from domain.enums import CanalPedido, StatusPedido, PerfilUsuario


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    perfil = Column(Enum(PerfilUsuario), default=PerfilUsuario.CLIENTE, nullable=False)
    # --- NOVO: Campo LGPD ---
    consentimento_lgpd = Column(Boolean, nullable=False, default=False)

    pedidos = relationship("Pedido", back_populates="cliente")


# --- Tabela de Itens do Pedido ---
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, nullable=False)  # Inteiro simples para o MVP não exigir tabela Produto
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="itens")


# ---------------------------------------

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    canal_pedido = Column(Enum(CanalPedido), nullable=False)
    status = Column(Enum(StatusPedido), default=StatusPedido.AGUARDANDO_PAGAMENTO, nullable=False)
    total = Column(Float, nullable=False)
    forma_pagamento = Column(String, nullable=False)
    data_criacao = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    cliente = relationship("Usuario", back_populates="pedidos")

    # --- Relacionamento com os itens ---
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")