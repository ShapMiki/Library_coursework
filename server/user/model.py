from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

from association.model import favorite_books



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    password: Mapped[str] = mapped_column(String(120))

    favorites = relationship(
        "Book",
        secondary=favorite_books,
        back_populates="fans",
    )
