from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.consumidor import Consumidor
from app.schemas.consumidor import ConsumidorCreate, ConsumidorUpdate, ConsumidorResponse

router = APIRouter(prefix="/consumidores", tags=["Consumidores"])


@router.get("/", response_model=List[ConsumidorResponse])
def listar_consumidores(
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    cidade: Optional[str] = Query(None, description="Filtrar por cidade"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Consumidor)
    if nome:
        query = query.filter(Consumidor.nome_consumidor.ilike(f"%{nome}%"))
    if cidade:
        query = query.filter(Consumidor.cidade.ilike(f"%{cidade}%"))
    if estado:
        query = query.filter(Consumidor.estado == estado.upper())
    return query.offset(skip).limit(limit).all()


@router.get("/{id_consumidor}", response_model=ConsumidorResponse)
def buscar_consumidor(id_consumidor: str, db: Session = Depends(get_db)):
    consumidor = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()
    if not consumidor:
        raise HTTPException(status_code=404, detail="Consumidor não encontrado")
    return consumidor


@router.post("/", response_model=ConsumidorResponse, status_code=201)
def criar_consumidor(consumidor: ConsumidorCreate, db: Session = Depends(get_db)):
    existente = db.query(Consumidor).filter(Consumidor.id_consumidor == consumidor.id_consumidor).first()
    if existente:
        raise HTTPException(status_code=400, detail="Consumidor com esse ID já existe")
    novo = Consumidor(**consumidor.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.put("/{id_consumidor}", response_model=ConsumidorResponse)
def atualizar_consumidor(id_consumidor: str, dados: ConsumidorUpdate, db: Session = Depends(get_db)):
    consumidor = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()
    if not consumidor:
        raise HTTPException(status_code=404, detail="Consumidor não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(consumidor, campo, valor)
    db.commit()
    db.refresh(consumidor)
    return consumidor


@router.delete("/{id_consumidor}", status_code=204)
def remover_consumidor(id_consumidor: str, db: Session = Depends(get_db)):
    consumidor = db.query(Consumidor).filter(Consumidor.id_consumidor == id_consumidor).first()
    if not consumidor:
        raise HTTPException(status_code=404, detail="Consumidor não encontrado")
    db.delete(consumidor)
    db.commit()