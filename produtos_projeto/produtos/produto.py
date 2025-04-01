from pydantic import BaseModel, field_validator
from typing import Optional

class Produto(BaseModel):
    id: Optional[int] = None  # ID é opcional (gerado pelo BD) e validado
    nome: str                 # Nome do produto (obrigatório e validado)
    preco: float              # Preço do produto (obrigatório e validado)
    estoque: int              # Quantidade em estoque (obrigatório e validado)

    @field_validator('id')
    def validar_id(cls, v):
        """Valida se o ID, caso fornecido, é um inteiro positivo."""
        if v is not None and v <= 0:
            raise ValueError('O id do produto não pode ser negativo ou zero.')
        return v

    @field_validator('nome')
    def validar_nome(cls, v):
        """Valida o nome do produto: não pode ser vazio e tem limite de caracteres."""
        nome_limpo = v.strip() # Remove espaços em branco extras
        if not nome_limpo:
            raise ValueError('O nome do produto não pode ser vazio.')
        if len(nome_limpo) > 100:
            raise ValueError('O nome do produto não pode exceder 100 caracteres.')
        return nome_limpo # Retorna o nome sem espaços extras

    @field_validator('preco')
    def validar_preco(cls, v):
        """Valida se o preço é um número positivo."""
        if v <= 0:
            raise ValueError('O preço deve ser maior que zero.')
        return v

    @field_validator('estoque')
    def validar_estoque(cls, v):
        """Valida se o estoque é um número não negativo."""
        if v < 0:
            raise ValueError('O estoque não pode ser negativo.')
        return v
