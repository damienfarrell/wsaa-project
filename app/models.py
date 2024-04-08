from datetime import datetime
from sqlalchemy import Text
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import expression
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    is_watched: Mapped[bool] = mapped_column(server_default=expression.false(), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("now()"))

    def __repr__(self) -> str:
        return f"<Note {self.title} at {self.created_at}>"
    
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("now()"))