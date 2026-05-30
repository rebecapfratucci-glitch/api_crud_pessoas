# app/main.py

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

import models
import crud
import schemas

from database import engine
from database import SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Cadastro de Pessoas",
    version="1.0.0"
)


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post(
    "/pessoas",
    response_model=schemas.PessoaResponse
)
def criar_pessoa(
    pessoa: schemas.PessoaCreate,
    db: Session = Depends(get_db)
):

    return crud.criar_pessoa(db, pessoa)


@app.get(
    "/pessoas",
    response_model=list[schemas.PessoaResponse]
)
def listar_pessoas(
    db: Session = Depends(get_db)
):

    return crud.listar_pessoas(db)


@app.get(
    "/pessoas/{pessoa_id}",
    response_model=schemas.PessoaResponse
)
def buscar_pessoa(
    pessoa_id: int,
    db: Session = Depends(get_db)
):

    pessoa = crud.buscar_por_id(db, pessoa_id)

    if not pessoa:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada"
        )

    return pessoa


@app.put(
    "/pessoas/{pessoa_id}",
    response_model=schemas.PessoaResponse
)
def atualizar_pessoa(
    pessoa_id: int,
    dados: schemas.PessoaUpdate,
    db: Session = Depends(get_db)
):

    pessoa = crud.atualizar_pessoa(
        db,
        pessoa_id,
        dados
    )

    if not pessoa:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada"
        )

    return pessoa


@app.delete("/pessoas/{pessoa_id}")
def excluir_pessoa(
    pessoa_id: int,
    db: Session = Depends(get_db)
):

    sucesso = crud.excluir_pessoa(
        db,
        pessoa_id
    )

    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada"
        )

    return {
        "mensagem": "Pessoa removida com sucesso"
    }