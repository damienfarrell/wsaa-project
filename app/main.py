
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.future import select
from sqlalchemy import update

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='wsaa-project',
                                user='postgres', password='***REMOVED***', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(4)

@app.get("/")
def read_root() -> str:
    return "Server is Running"

@app.get("/films")
def read_films(db: Session = Depends(get_db)):
    statement = select(models.Film)
    result = db.execute(statement).scalars().all()
    return {"data": result}

@app.post("/films", status_code=status.HTTP_201_CREATED)
def create_films(film: schemas.FilmSchema, db: Session = Depends(get_db)):
    new_film = models.Film(**film.model_dump())
    db.add(new_film)
    db.commit()
    db.refresh(new_film)
    return {"data": new_film}

@app.get("/films/{id}")
def read_film_by_id(id: int, db: Session = Depends(get_db)):
    statement = select(models.Film).where(models.Film.id == id)
    result = db.execute(statement).scalars().one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film with id: {id} was not found")
    return {"data" : result}

@app.delete("/films/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_film(id: int, db: Session = Depends(get_db)):
    # Find the film by id
    statement = select(models.Film).where(models.Film.id == id)
    film_to_delete = db.execute(statement).scalars().one_or_none()
    if film_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film with id: {id} does not exist")
    db.delete(film_to_delete)
    db.commit()

@app.put("/films/{id}")
def update_film(id: int, film: schemas.FilmSchema, db: Session = Depends(get_db)):
    updated_film_data = film.model_dump(exclude_unset=True)
    statement = update(models.Film).where(models.Film.id == id).values(**updated_film_data)
    result = db.execute(statement)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film with id: {id} does not exist")
    db.commit()
    statement = select(models.Film).where(models.Film.id == id)
    updated_film = db.execute(statement).scalars().first()
    return updated_film