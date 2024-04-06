from typing import Union
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Film(BaseModel):
    # id: int
    title: str
    is_watched: Union[bool, None] = None
    rating: Union[int, None] = None
    comment: Union[str, None] = None


while True:
    try:

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

@app.post("/films", status_code=status.HTTP_201_CREATED)
def create_films(film: Film):
    cursor.execute("""INSERT INTO films (title) VALUES (%s) RETURNING *""", (film.title,))
    new_film = cursor.fetchone()
    conn.commit()
    return {"data": new_film}

@app.get("/films/{id}")
def read_film(id: int):
    cursor.execute("""SELECT * FROM films WHERE id = %s""", (id,))
    film = cursor.fetchone()
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"film with id: {id} was not found")
    return {"data" : film}

@app.delete("/films/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_film(id: int):
    cursor.execute("""DELETE FROM films WHERE id = %s RETURNING *""", (id,))
    deleted_film = cursor.fetchone()
    conn.commit()
    if deleted_film == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#### TODO I need to change and update the SQL statments on POST and PUT

@app.put("/films/{id}")
def update_film(id: int, film: Film):
    cursor.execute("""UPDATE films SET title = %s WHERE id = %s RETURNING *""", (film.title, id))
    updated_film = cursor.fetchone()
    conn.commit()
    if updated_film == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {"data" : updated_film}