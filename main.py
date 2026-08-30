from fastapi import FastAPI
from infrastructure.database import engine
from domain import models
from api.rotas import router

# Cria as tabelas no banco de dados SQLite automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Raízes do Nordeste",
    description="API para gestão de pedidos e multicanalidade da rede Raízes do Nordeste",
    version="1.0.0"
)

# Conecta as rotas que criei na aplicação principal
app.include_router(router)