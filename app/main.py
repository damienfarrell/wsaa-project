from typing import Union
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Film(BaseModel):
    id: int
    title: str
    watched: Union[bool, None] = None
    review: Union[int, None] = None
    comment: Union[str, None] = None

while True:
    try:
        conn = psycopg2.connect()
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
def read_films():
    cursor.execute("""SELECT * FROM films""")
    films = cursor.fetchall()
    return {"data": films}

@app.get("/films/{id}")
def read_film(id: int):
    return {"film_id": id, "message": "Film data goes here"}

@app.post("/films/{id}")
def create_film(film: Film):
    return {"film_id": film.id, "film_name": film}

@app.put("/films/{id}")
def update_film(film: Film):
    return {"film_id": film.id, "film_name": film}

@app.delete("/films/{id}")
def delete_film(film: Film):
    return {"film_id": film.id, "film_name": film}

