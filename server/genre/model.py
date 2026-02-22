from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base



class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)

    books = relationship("Book", back_populates="genre")
