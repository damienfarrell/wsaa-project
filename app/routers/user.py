from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Request, Header
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

templates = Jinja2Templates(directory="templates")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(request: Request, user: schemas.UserCreate, hx_request: Optional[str] = Header(None), db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    if hx_request:
        return templates.TemplateResponse("index.html", {"request": request})
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    statement = select(models.User).where(models.User.id == id)
    result = db.execute(statement).scalars().one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return result