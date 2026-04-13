from typing import Optional
from pydantic import BaseModel


class ConsumidorBase(BaseModel):
    prefixo_cep: str
    nome_consumidor: str
    cidade: str
    estado: str


class ConsumidorCreate(ConsumidorBase):
    id_consumidor: str


class ConsumidorUpdate(BaseModel):
    prefixo_cep: Optional[str] = None
    nome_consumidor: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None


class ConsumidorResponse(ConsumidorBase):
    id_consumidor: str

    class Config:
        from_attributes = True