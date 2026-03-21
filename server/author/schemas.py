from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

from config import settings


class SAuthor(BaseModel):
    name: str
