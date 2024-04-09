from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update
from typing import List
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/films",
    tags=["Films"]
)

@router.get("/", response_model=List[schemas.FilmSchemaResponse])
def read_films(db: Session = Depends(get_db)):
    statement = select(models.Film)
    result = db.execute(statement).scalars().all()
    return result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.FilmSchemaResponse)
def create_films(film: schemas.CreateFilm, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_film = models.Film(**film.model_dump())
    db.add(new_film)
    db.commit()
    db.refresh(new_film)
    return new_film

@router.get("/{id}", response_model=schemas.FilmSchemaResponse)
def read_film_by_id(id: int, db: Session = Depends(get_db)):
    statement = select(models.Film).where(models.Film.id == id)
    result = db.execute(statement).scalars().one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film with id: {id} was not found")
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_film(id: int, db: Session = Depends(get_db)):
    # Find the film by id
    statement = select(models.Film).where(models.Film.id == id)
    film_to_delete = db.execute(statement).scalars().one_or_none()
    if film_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film with id: {id} does not exist")
    db.delete(film_to_delete)
    db.commit()

@router.put("/{id}", response_model=schemas.FilmSchemaResponse)
def update_film(id: int, film: schemas.UpdateFilm, db: Session = Depends(get_db)):
    updated_film_data = film.model_dump(exclude_unset=True)
    statement = update(models.Film).where(models.Film.id == id).values(**updated_film_data)
    result = db.execute(statement)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film with id: {id} does not exist")
    db.commit()
    statement = select(models.Film).where(models.Film.id == id)
    updated_film = db.execute(statement).scalars().first()
    return updated_film