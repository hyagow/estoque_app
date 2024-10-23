# type: ignore
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Produto(BaseModel):
    nome: str
    categoria: str
    quantidade: int
    preco: float
    localizacao: str
