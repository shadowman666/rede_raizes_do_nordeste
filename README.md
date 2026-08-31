# Rede Raízes do Nordeste - API RESTful

API RESTful desenvolvida em Python com **FastAPI** para o gerenciamento do sistema de pedidos multicanal da Rede Raízes do Nordeste. Projeto desenvolvido como requisito prático acadêmico do curso de Análise e Desenvolvimento de Sistemas da Uninter.

---

## Stack Tecnológica e Requisitos de Ambiente

* **Linguagem:** Python 3.10+
* **Framework Web:** FastAPI (v0.100+)
* **Servidor ASGI:** Uvicorn
* **ORM:** SQLAlchemy
* **Banco de Dados:** SQLite (`raizes.db`)
* **Validação de Dados:** Pydantic v2
* **Segurança:** JWT (`python-jose`) e Hash de senhas (`passlib` com `bcrypt`)
* **Testes e Documentação:** Postman & OpenAPI (Swagger UI)

---

## Estrutura do Projeto

```text
rede_raizes_do_nordeste/
├── api/                  # Controladores, rotas e dependências
│   ├── dependecias.py    # Middleware e injeção do usuário autenticado (RBAC)
│   └── rotas.py          # Endpoints (/usuarios, /auth/login, /pedidos, /admin)
├── application/          # Regras de negócio e segurança
│   └── security.py       # Criptografia, geração e validação de tokens JWT
├── domain/               # Entidades de domínio, contratos e enums
│   ├── enums.py          # Enums de canais, perfis e status do pedido
│   ├── models.py         # Modelos de tabelas ORM (SQLAlchemy) com relação 1:N
│   └── schemas.py        # Esquemas de entrada/saída (Pydantic)
├── infrastructure/       # Configurações de infraestrutura
│   ├── database.py       # Engine de conexão e sessão do SQLite
│   └── logger.py         # Módulo de auditoria e logs de ações sensíveis
├── postman/              # Artefatos de testes de API
│   └── Rede Raizes do Nordeste.postman_collection.json
├── .env.example          # Modelo de variáveis de ambiente
├── main.py               # Ponto de entrada da aplicação
├── raizes.db             # Banco de dados relacional SQLite
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação técnica de execução
```

---

## Guia de Instalação e Execução Local

### 1. Clonar o Repositório
```bash
git clone https://github.com/shadowman666/rede_raizes_do_nordeste.git
cd rede_raizes_do_nordeste
```

### 2. Configurar o Ambiente Virtual (venv)

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
O projeto utiliza configurações padrão embutidas para o ambiente de desenvolvimento. Para customizar parâmetros, crie o arquivo `.env` baseado no modelo:

**Windows (PowerShell):**
```powershell
copy .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

### 5. Criação do Banco de Dados
A aplicação utiliza o **SQLAlchemy** integrado ao SQLite. As tabelas (`usuarios`, `pedidos` e `itens_pedido`) e o arquivo `raizes.db` são criados e inicializados de forma **automática** na primeira execução da API, dispensando migrations manuais no escopo do MVP.

### 6. Iniciar a API
```bash
uvicorn main:app --reload
```
A API estará acessível em: `http://localhost:8000`

---

## Documentação Interativa (OpenAPI)

Com o servidor em execução, acesse a documentação interativa pelo navegador:

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Endpoints e Regras de Negócio

| Método | Rota | Autenticação | Descrição |
| :--- | :--- | :--- | :--- |
| `POST` | `/usuarios` | Pública | Cadastra cliente/admin com hash `bcrypt` e aceite obrigatório de LGPD. |
| `POST` | `/auth/login` | Pública | Autentica usuário e retorna Token JWT Bearer com perfil integrado. |
| `POST` | `/pedidos` | **Bearer Token** | Registra pedido multicanal com itens e simula pagamento síncrono. |
| `GET` | `/pedidos` | **Bearer Token** | Lista o histórico de pedidos exclusivo do próprio cliente autenticado. |
| `GET` | `/admin/pedidos` | **Bearer Token (ADMIN)** | Lista todos os pedidos da rede, restrito por controle de acesso (RBAC). |

---

## Exemplos de Payloads (JSON)

### 1. Cadastro de Usuário com Consentimento LGPD (`POST /usuarios`)
O envio do campo `"consentimento_lgpd": true` é **obrigatório**. Se omitido ou enviado como `false`, a API rejeita a requisição com `HTTP 400 Bad Request`:

```json
{
  "nome": "Carlos Lavratti",
  "email": "carlos.lavratti@gmail.com",
  "senha": "Teste12345678",
  "consentimento_lgpd": true,
  "perfil": "CLIENTE"
}
```

### 2. Criação de Pedido Multicanal com Itens (`POST /pedidos`)
O cálculo do valor total do pedido é realizado de forma automática no back-end a partir do array `"itens"`:

```json
{
  "canal_pedido": "APP",
  "forma_pagamento": "PIX",
  "itens": [
    {
      "produto_id": 12,
      "quantidade": 2,
      "preco_unitario": 25.50
    }
  ]
}
```

---

## Simulação de Gateway de Pagamento (Mock)

* **Pagamento Aprovado:** Enviar qualquer forma regular em `forma_pagamento` (ex.: `"PIX"`, `"CARTAO"`) processa a cobrança, retorna status **`201 Created`** e registra o pedido como **`PAGO`**.
* **Pagamento Recusado:** Enviar `"forma_pagamento": "ERRO"` aciona a recusa simulada no gateway mock, retornando status **`402 Payment Required`** e persistindo o status como **`CANCELADO`**.

---

## Execução dos Testes Automatizados (Postman)

A suíte de testes cobre **13 cenários funcionais** (positivos e negativos) organizados por recursos para validação completa da API, controle de perfis (RBAC) e regras de negócio.

### Como importar e rodar a suíte no Postman:
1. Abra o **Postman**.
2. Clique no botão **Import** (canto superior esquerdo).
3. Selecione o arquivo localizado em: `postman/Rede Raizes do Nordeste.postman_collection.json`.
4. Execute as requisições na ordem sugerida:
   * **Usuarios:** `T09` (Criação de usuário com LGPD), `T10` (Rejeição de e-mail duplicado) e `T11` (Cadastro de ADMIN).
   * **Auth:** `T01` (Login válido e token JWT) e `T03` (Bloqueio por senha incorreta).
   * **Pedidos:** `T02` (Acesso sem token), `T04` (Campo obrigatório ausente), `T05` (Tipo de dado inválido), `T06` (Token adulterado), `T07` (Pagamento aprovado) e `T08` (Pagamento recusado).
   * **Consultas:** `T12` (Listar Meus Pedidos do Cliente) e `T13` (Listar Todos os Pedidos - Gestão Admin).