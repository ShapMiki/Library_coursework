from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base



class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))

    books = relationship("Book", back_populates="author")
