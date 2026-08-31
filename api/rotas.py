from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from domain.schemas import UsuarioCreate, UsuarioResponse, Token, PedidoCreate, PedidoResponse
from domain.models import Usuario, Pedido, ItemPedido
from domain.enums import StatusPedido
from application.security import gerar_hash_senha, verificar_senha, criar_token_acesso
from api.dependecias import obter_usuario_logado, obter_usuario_admin

router = APIRouter()

# ==========================================
# 1. ROTA DE CADASTRO DE USUÁRIO
# ==========================================
@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if not usuario.consentimento_lgpd:
        raise HTTPException(status_code=400,
                            detail={"error": "LGPD_REJEITADA", "message": "O consentimento dos termos da LGPD é obrigatório."})

    # Verifico se já existe um usuário com este e-mail no meu banco de dados
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400,
                            detail={"error": "EMAIL_EXISTENTE", "message": "Este e-mail já está em uso."})

    # Crio a entidade do novo usuário
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        # LGPD: Optei por salvar apenas o hash no banco, garantindo a proteção da senha do cliente
        senha_hash=gerar_hash_senha(usuario.senha),
        consentimento_lgpd=usuario.consentimento_lgpd,
        perfil=usuario.perfil
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

# ==========================================
# 2. ROTA DE LOGIN (Gera o Token)
# ==========================================
@router.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Busco o usuário no banco pelo e-mail
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    # Verifico se o usuário existe e se a senha que ele digitou bate com o meu hash
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "CREDENCIAIS_INVALIDAS", "message": "E-mail ou senha incorretos."},
        )

    # Gero o token de acesso que criei para as rotas protegidas
    token = criar_token_acesso(dados={"email": usuario.email, "perfil": usuario.perfil})
    return {"access_token": token, "token_type": "bearer"}

# ==========================================
# 3. ROTA DE PEDIDO (Fluxo Crítico + Mock de Pagamento)
# ==========================================
@router.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(
        pedido_in: PedidoCreate,
        db: Session = Depends(get_db),
        usuario_atual: Usuario = Depends(obter_usuario_logado)
):
    # Calcula o total real multiplicando quantidade x preço de cada item
    total_calculado = sum(item.quantidade * item.preco_unitario for item in pedido_in.itens)

    # 1. Registro o pedido inicial com a situação "Aguardando Pagamento"
    novo_pedido = Pedido(
        canal_pedido=pedido_in.canal_pedido,
        total=total_calculado,
        forma_pagamento=pedido_in.forma_pagamento,
        cliente_id=usuario_atual.id,
        status=StatusPedido.AGUARDANDO_PAGAMENTO
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    # 2. Insiro todos os itens do pedido no banco de dados
    for item in pedido_in.itens:
        novo_item = ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=item.preco_unitario
        )
        db.add(novo_item)
    db.commit()
    db.refresh(novo_pedido)

    # 3. MOCK DE PAGAMENTO (Simulação)
    if pedido_in.forma_pagamento.upper() == "ERRO":
        novo_pedido.status = StatusPedido.CANCELADO
        db.commit()
        raise HTTPException(
            status_code=402,
            detail={"error": "PAGAMENTO_RECUSADO", "message": "Pagamento recusado pelo serviço externo simulado."}
        )

    # Se aprovado, muda para PAGO
    novo_pedido.status = StatusPedido.PAGO
    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido

# ==========================================
# 4. ROTA DE CONSULTA DO CLIENTE
# ==========================================
@router.get("/pedidos", response_model=list[PedidoResponse])
def listar_meus_pedidos(db: Session = Depends(get_db), usuario_atual: Usuario = Depends(obter_usuario_logado)):
    """Retorna apenas os pedidos do cliente logado."""
    return db.query(Pedido).filter(Pedido.cliente_id == usuario_atual.id).all()

# ==========================================
# 5. ROTA GERENCIAL ADMIN (RBAC)
# ==========================================
@router.get("/admin/pedidos", response_model=list[PedidoResponse], dependencies=[Depends(obter_usuario_admin)])
def listar_todos_pedidos_admin(db: Session = Depends(get_db)):
    """Retorna todos os pedidos. Exige perfil ADMIN."""
    return db.query(Pedido).all()