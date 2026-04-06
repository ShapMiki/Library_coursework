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

@router.get("/all")
async def get_all_authors():
    # Предполагается, что в AuthorDAO есть метод find_all
    authors = await AuthorDAO.find_all()
    # Возвращаем список словарей с id и name
    return [{"id": a.id, "name": a.name} for a in authors]
