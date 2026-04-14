from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoResponse

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.get("/", response_model=List[PedidoResponse])
def listar_pedidos(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    id_consumidor: Optional[str] = Query(None, description="Filtrar por consumidor"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Pedido)
    
    if status:
        query = query.filter(Pedido.status.ilike(f"%{status}%"))
    if id_consumidor:
        query = query.filter(Pedido.id_consumidor == id_consumidor)
    
    # O selectinload carrega todos os itens de todos os pedidos em apenas 2 queries
    return query.options(selectinload(Pedido.itens)).offset(skip).limit(limit).all()


@router.get("/{id_pedido}", response_model=PedidoResponse)
def buscar_pedido(id_pedido: str, db: Session = Depends(get_db)):
    # Usamos o selectinload aqui também para carregar os itens automaticamente
    pedido = (
        db.query(Pedido)
        .options(selectinload(Pedido.itens))
        .filter(Pedido.id_pedido == id_pedido)
        .first()
    )
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@router.post("/", response_model=PedidoResponse, status_code=201)
def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    existente = db.query(Pedido).filter(Pedido.id_pedido == pedido.id_pedido).first()
    if existente:
        raise HTTPException(status_code=400, detail="Pedido com esse ID já existe")
    
    novo = Pedido(**pedido.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    
    # Retornamos o objeto; o Pydantic cuidará da lista de itens vazia
    return novo


@router.put("/{id_pedido}", response_model=PedidoResponse)
def atualizar_pedido(id_pedido: str, dados: PedidoUpdate, db: Session = Depends(get_db)):
    pedido = (
        db.query(Pedido)
        .options(selectinload(Pedido.itens))
        .filter(Pedido.id_pedido == id_pedido)
        .first()
    )
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(pedido, campo, valor)
    
    db.commit()
    db.refresh(pedido)
    return pedido


@router.delete("/{id_pedido}", status_code=204)
def remover_pedido(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    db.delete(pedido)
    db.commit()