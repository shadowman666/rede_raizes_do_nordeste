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

## Execução Local

Como esta é uma API de back-end desenvolvida para execução local, siga os passos abaixo para inicializar o ambiente e testar os endpoints:

1. Instale as dependências do projeto:

   pip install -r requirements.txt
   
2. Inicie o servidor da API utilizando o Uvicorn:

    uvicorn main:app --reload

3. Com o servidor rodando em sua máquina, acesse a documentação interativa Swagger/OpenAPI pelo navegador no endereço:

    http://localhost:8000/docs