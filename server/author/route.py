from fastapi import APIRouter, Request, Response, status, Depends

from author.schemas import SAuthor
from author.dao import AuthorDAO

router = APIRouter(
    prefix="/author",
    tags=["author"],
)


@router.post("/")
async def create_author(author: SAuthor):
    # Используем созданный DAO для записи в базу
    new_author = await AuthorDAO.add_one(author)
    return new_author