from fastapi import FastAPI
from . import models
from .database import engine
from .routers import film, user, auth

app = FastAPI()

app.include_router(film.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root() -> str:
    return "Server is Running"