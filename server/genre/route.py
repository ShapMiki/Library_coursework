from fastapi import APIRouter, Request, Response, status, Depends
from fastapi.exceptions import HTTPException

from genre.dao import GenreDAO
from genre.schemas import *



router = APIRouter(
    prefix="/genre",
    tags=["genre"],
)


@router.post("/")
async def create_genre(genre: SGenre):
    new_genre = await GenreDAO.add_one(genre)
    return new_genre

@router.get("/all")
async def get_all_genres():
    genres = await GenreDAO.find_all()
    return [{"id": g.id, "name": g.name} for g in genres]

@router.get("/{genre_id}")
async def get_genre(genre_id: int):
    genre = await GenreDAO.find_one_or_none(id=genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    return {"id": genre.id, "name": genre.name}

# 4. Редактирование
@router.post("/edit")
async def edit_genre(data: SGenreEdit):
    # Превращаем объекты Pydantic в словари для DAO
    genre_list = data.genre_data
    updated = await GenreDAO.update_one(genre_list)
    if not updated:
        raise HTTPException(status_code=404, detail="Ошибка обновления")
    return updated

# 5. Удаление
@router.delete("/{genre_id}")
async def delete_genre(genre_id: int):
    result = await GenreDAO.delete_by_id(genre_id)
    if not result:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    return {"status": "success"}