from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Request, Header
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, oauth2

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/films",
    tags=["Films"]
)

@router.get("/", response_model=List[schemas.FilmSchemaResponse])
def read_films(request: Request, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
               limit: int = 50, skip: int = 0, search: Optional[str] = ""):
    statement = select(models.Film).where(models.Film.user_id == current_user.id, models.Film.title.contains(search)).limit(limit).offset(skip)
    result = db.execute(statement).scalars().all()
    if hx_request:
        return templates.TemplateResponse("partials/film_table.html", {"request": request, "films": result, "current_user": current_user})
    return result

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.FilmSchemaResponse)
def create_films(film: schemas.CreateFilm, request: Request, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), hx_request: Optional[str] = Header(None)):
    new_film = models.Film(user_id=current_user.id, **film.model_dump())
    db.add(new_film)
    db.commit()
    db.refresh(new_film)
    if hx_request:
        return templates.TemplateResponse("partials/film_row.html", {"request": request, "film": new_film})
    return new_film

@router.get("/{id}", response_model=schemas.FilmSchemaResponse)
def read_film_by_id(request: Request, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    statement = select(models.Film).where(models.Film.id == id, models.Film.user_id == current_user.id)
    result = db.execute(statement).scalars().one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film with id: {id} was not found")
    if "text/html" in request.headers.get("accept", ""):
        return templates.TemplateResponse("index.html", {"request": request, "film": result})
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_film(request: Request, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), hx_request: Optional[str] = Header(None)):
    statement = select(models.Film).where(models.Film.id == id)
    film_to_delete = db.execute(statement).scalars().one_or_none()
    if film_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film with id: {id} does not exist")
    if film_to_delete.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    db.delete(film_to_delete)
    db.commit()

@router.put("/{id}", response_model=schemas.FilmSchemaResponse)
def update_film(request: Request, id: int, film: schemas.UpdateFilm, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), hx_request: Optional[str] = Header(None)):
    updated_film_data = film.model_dump(exclude_unset=True)
    existing_film = db.execute(
        select(models.Film).where(models.Film.id == id)
    ).scalars().one_or_none()
    if not existing_film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Film with id: {id} does not exist")
    if existing_film.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    statement = update(models.Film).where(models.Film.id == id).values(**updated_film_data)
    db.execute(statement)
    db.commit()
    updated_film = db.execute(
        select(models.Film).where(models.Film.id == id)
    ).scalars().first()
    if hx_request:
        if film.is_watched is not None:
            return templates.TemplateResponse("partials/film_row.html", {"request": request, "film": updated_film})
        else:
            statement = update(models.Film).where(models.Film.id == id).values(is_watched=False)
            db.execute(statement)
            db.commit()
            updated_film = db.execute(
                select(models.Film).where(models.Film.id == id)
            ).scalars().first()
            return templates.TemplateResponse("partials/film_row.html", {"request": request, "film": updated_film})
    return updated_film