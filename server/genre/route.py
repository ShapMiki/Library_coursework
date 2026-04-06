from fastapi import APIRouter, Request, Response, status, Depends

from genre.dao import GenreDAO
from genre.schemas import SGenre



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

