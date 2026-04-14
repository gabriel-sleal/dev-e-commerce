from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.produto import Produto
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.models.item_pedido import ItemPedido
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    nome: Optional[str] = Query(None, description="Buscar por nome"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Produto)

    if categoria:
        query = query.filter(Produto.categoria_produto.ilike(f"%{categoria}%"))
    if nome:
        query = query.filter(Produto.nome_produto.ilike(f"%{nome}%"))

    produtos = query.offset(skip).limit(limit).all()

    ids = [p.id_produto for p in produtos]
    medias = (
        db.query(ItemPedido.id_produto, func.avg(AvaliacaoPedido.avaliacao))
        .join(AvaliacaoPedido, AvaliacaoPedido.id_pedido == ItemPedido.id_pedido)
        .filter(ItemPedido.id_produto.in_(ids))
        .group_by(ItemPedido.id_produto)
        .all()
    )
    medias_dict = {id_produto: round(media, 2) for id_produto, media in medias}

    return [
        {
            "id_produto": p.id_produto,
            "nome_produto": p.nome_produto,
            "categoria_produto": p.categoria_produto,
            "peso_produto_gramas": p.peso_produto_gramas,
            "comprimento_centimetros": p.comprimento_centimetros,
            "altura_centimetros": p.altura_centimetros,
            "largura_centimetros": p.largura_centimetros,
            "media_avaliacoes": medias_dict.get(p.id_produto),
        }
        for p in produtos
    ]


@router.get("/{id_produto}", response_model=ProdutoResponse)
def buscar_produto(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    media = _calcular_media(id_produto, db)

    return {
        "id_produto": produto.id_produto,
        "nome_produto": produto.nome_produto,
        "categoria_produto": produto.categoria_produto,
        "peso_produto_gramas": produto.peso_produto_gramas,
        "comprimento_centimetros": produto.comprimento_centimetros,
        "altura_centimetros": produto.altura_centimetros,
        "largura_centimetros": produto.largura_centimetros,
        "media_avaliacoes": media,
    }


@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    existente = db.query(Produto).filter(Produto.id_produto == produto.id_produto).first()
    if existente:
        raise HTTPException(status_code=400, detail="Produto com esse ID já existe")

    novo = Produto(**produto.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {**novo.__dict__, "media_avaliacoes": None}


@router.put("/{id_produto}", response_model=ProdutoResponse)
def atualizar_produto(id_produto: str, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)
    media = _calcular_media(id_produto, db)
    return {**produto.__dict__, "media_avaliacoes": media}


@router.delete("/{id_produto}", status_code=204)
def remover_produto(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()


def _calcular_media(id_produto: str, db: Session) -> Optional[float]:
    resultado = (
        db.query(func.avg(AvaliacaoPedido.avaliacao))
        .join(ItemPedido, AvaliacaoPedido.id_pedido == ItemPedido.id_pedido)
        .filter(ItemPedido.id_produto == id_produto)
        .scalar()
    )
    return round(resultado, 2) if resultado else None