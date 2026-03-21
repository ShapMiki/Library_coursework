from sqlalchemy import insert
from basedao.dao import BaseDAO
from database import async_session_maker
from genre.model import Genre

class GenreDAO(BaseDAO):
    model = Genre

    @classmethod
    async def add_one(cls, genre_data):
        async with async_session_maker() as session:
            orm_genre = Genre(name=genre_data.name)
            session.add(orm_genre)
            await session.commit()
            await session.refresh(orm_genre)
            return orm_genre
