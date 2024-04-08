from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update
from typing import List
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    statement = select(models.User).where(models.User.email == user_credentials.email)
    user = db.execute(statement).scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    return {"token" : "example token"}