from typing import Optional
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

from association.model import favorite_books



class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(200))

    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("authors.id"), nullable=True)
    genre_id: Mapped[Optional[int]] = mapped_column(ForeignKey("genres.id"), nullable=True)

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")

    extra_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    fans = relationship(
        "User",
        secondary="favorite_books",
        back_populates="favorites",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author_id": self.author_id,
            "genre_id": self.genre_id,
            "author": self.author.name,
            "genre": self.genre.name,
            "extra_data": self.extra_data or {}
        }
