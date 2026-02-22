from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

favorite_books = Table(
    "favorite_books",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)


