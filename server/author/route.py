from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from typing import List

from author.schemas import SAuthor, SAuthorEdit
from author.dao import AuthorDAO

router = APIRouter(
    prefix="/author",
    tags=["author"],
)

# 1. Создание автора
@router.post("/")
async def create_author(author: SAuthor):
    new_author = await AuthorDAO.add_one(author)
    return new_author

# 2. Получение всех авторов
@router.get("/all")
async def get_all_authors():
    authors = await AuthorDAO.find_all()
    return [{"id": a.id, "name": a.name} for a in authors]

# 3. Получение одного автора по ID (для загрузки в форму)
@router.get("/{author_id}")
async def get_author(author_id: int):
    author = await AuthorDAO.find_one_or_none(id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return {"id": author.id, "name": author.name}

# 4. Редактирование (совпадает с логикой book_data)
@router.post("/edit")
async def edit_author(data: SAuthorEdit):
    # Превращаем Pydantic-объекты в словари для DAO
    author_list = [item.dict() for item in data.author_data]
    updated = await AuthorDAO.update_one(author_list)
    if not updated:
        raise HTTPException(status_code=404, detail="Ошибка при обновлении автора")
    return updated

# 5. Удаление автора
@router.delete("/{author_id}")
async def delete_author(author_id: int):
    result = await AuthorDAO.delete_by_id(author_id)
    if not result:
        raise HTTPException(status_code=404, detail="Не удалось удалить автора")
    return {"status": "success"}