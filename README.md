# Rede Raízes do Nordeste - Backend

API RESTful desenvolvida em Python com FastAPI para o gerenciamento do sistema de pedidos multicanal da Rede Raízes do Nordeste, desenvolvida como parte de trabalho acadêmico da Uninter.

## Stack Tecnológica
* **Linguagem:** Python 3.x
* **Framework Web:** FastAPI
* **ORM:** SQLAlchemy
* **Banco de Dados:** SQLite
* **Validação:** Pydantic com Enums estritos
* **Segurança:** Autenticação baseada em tokens JWT

## Estrutura de Pastas (Arquitetura Modular)
* `domain/`: Modelos de domínio, definições de Enum e contratos de validação (schemas.py).
* `application/`: Camada de serviços e regras de negócio/segurança (JWT).
* `infrastructure/`: Configuração de conexão com o banco de dados e modelos ORM.
* `api/`: Controladores e mapeamento de rotas RESTful.

## Execução
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt