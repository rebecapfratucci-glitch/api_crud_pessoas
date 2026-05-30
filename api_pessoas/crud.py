# app/crud.py

from sqlalchemy.orm import Session

import models
import schemas


def criar_pessoa(db: Session, pessoa: schemas.PessoaCreate):

    nova = models.Pessoa(**pessoa.model_dump())

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


def listar_pessoas(db: Session):

    return db.query(models.Pessoa).all()


def buscar_por_id(db: Session, pessoa_id: int):

    return (
        db.query(models.Pessoa)
        .filter(models.Pessoa.id == pessoa_id)
        .first()
    )


def atualizar_pessoa(
    db: Session,
    pessoa_id: int,
    dados: schemas.PessoaUpdate
):

    pessoa = buscar_por_id(db, pessoa_id)

    if not pessoa:
        return None

    for campo, valor in dados.model_dump().items():
        setattr(pessoa, campo, valor)

    db.commit()
    db.refresh(pessoa)

    return pessoa


def excluir_pessoa(db: Session, pessoa_id: int):

    pessoa = buscar_por_id(db, pessoa_id)

    if not pessoa:
        return False

    db.delete(pessoa)
    db.commit()

    return True