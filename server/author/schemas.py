from pydantic import BaseModel
from typing import Optional, List

class SAuthor(BaseModel):
    id: Optional[int] = None
    name: str

class SAuthorEdit(BaseModel):
    author_data: List[SAuthor]