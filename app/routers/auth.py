from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(tags=["Authentication"])

templates = Jinja2Templates(directory="templates")

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    statement = select(models.User).where(models.User.email == user_credentials.username)
    user = db.execute(statement).scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    return {"access_token" : access_token, "token_type" : "bearer"}

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})