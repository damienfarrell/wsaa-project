from datetime import datetime
from typing import Union, Optional
from pydantic import BaseModel, EmailStr

class FilmSchemaBase(BaseModel):
    title: str
    is_watched: Union[bool, None] = None
    rating: Union[int, None] = None
    comment: Union[str, None] = None

class CreateFilm(FilmSchemaBase):
    pass

class UpdateFilm(FilmSchemaBase):
    pass

class FilmSchemaResponse(FilmSchemaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class  UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None