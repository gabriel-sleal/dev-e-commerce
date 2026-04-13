from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vendedor import Vendedor
from app.schemas.vendedor import VendedorCreate, VendedorUpdate, VendedorResponse

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])


@router.get("/", response_model=List[VendedorResponse])
def listar_vendedores(
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    cidade: Optional[str] = Query(None, description="Filtrar por cidade"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Vendedor)
    if nome:
        query = query.filter(Vendedor.nome_vendedor.ilike(f"%{nome}%"))
    if cidade:
        query = query.filter(Vendedor.cidade.ilike(f"%{cidade}%"))
    if estado:
        query = query.filter(Vendedor.estado == estado.upper())
    return query.offset(skip).limit(limit).all()


@router.get("/{id_vendedor}", response_model=VendedorResponse)
def buscar_vendedor(id_vendedor: str, db: Session = Depends(get_db)):
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    return vendedor


@router.post("/", response_model=VendedorResponse, status_code=201)
def criar_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):
    existente = db.query(Vendedor).filter(Vendedor.id_vendedor == vendedor.id_vendedor).first()
    if existente:
        raise HTTPException(status_code=400, detail="Vendedor com esse ID já existe")
    novo = Vendedor(**vendedor.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.put("/{id_vendedor}", response_model=VendedorResponse)
def atualizar_vendedor(id_vendedor: str, dados: VendedorUpdate, db: Session = Depends(get_db)):
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(vendedor, campo, valor)
    db.commit()
    db.refresh(vendedor)
    return vendedor


@router.delete("/{id_vendedor}", status_code=204)
def remover_vendedor(id_vendedor: str, db: Session = Depends(get_db)):
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == id_vendedor).first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    db.delete(vendedor)
    db.commit()