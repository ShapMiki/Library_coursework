from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from config import settings


class SBook(BaseModel):
    title: str
    description: str
    author_id: Optional[int] = None
    genre_id: Optional[int] = None
    extra_data: Optional[dict] = None

    class Config:
        orm_mode = True

class SBookDataSet(BaseModel):
    book_data: Optional[list] = None

