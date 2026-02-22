from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from config import settings


class SBook(BaseModel):
    title: str
    description: str
    author_id: Optional[int] = None
    genre_id: Optional[int] = None

    class Config:
        orm_mode = True
