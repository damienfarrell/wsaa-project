from typing import Union
from pydantic import BaseModel


class FilmSchema(BaseModel):
    # id: int
    title: str
    is_watched: Union[bool, None] = None
    rating: Union[int, None] = None
    comment: Union[str, None] = None