# app/schemas.py

from pydantic import BaseModel, EmailStr

class PessoaBase(BaseModel):

    nome: str
    sobrenome: str

    email: EmailStr
    whatsapp: str

    cep: str
    rua: str
    numero: str
    complemento: str | None = None
    bairro: str
    cidade: str
    estado: str

    observacoes: str | None = None


class PessoaCreate(PessoaBase):
    pass


class PessoaUpdate(PessoaBase):
    pass


class PessoaResponse(PessoaBase):
    id: int

    class Config:
        from_attributes = True