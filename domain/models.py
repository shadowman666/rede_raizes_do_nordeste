from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
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
    perfil = Column(
        Enum(PerfilUsuario), default=PerfilUsuario.CLIENTE, nullable=False
    )

    # Relacionamento: Permito que um usuário tenha múltiplos pedidos associados
    pedidos = relationship("Pedido", back_populates="cliente")


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    canal_pedido = Column(
        Enum(CanalPedido), nullable=False
    )  # Multicanalidade (APP, TOTEM, etc.)
    status = Column(
        Enum(StatusPedido),
        default=StatusPedido.AGUARDANDO_PAGAMENTO,
        nullable=False,
    )
    total = Column(Float, nullable=False)
    forma_pagamento = Column(String, nullable=False)  # Ex: MOCK, PIX, CARTAO
    data_criacao = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),  # Padrão UTC moderno
    )

    # Chave estrangeira ligando o pedido ao cliente
    cliente_id = Column(Integer, ForeignKey("usuarios.id"))
    cliente = relationship("Usuario", back_populates="pedidos")