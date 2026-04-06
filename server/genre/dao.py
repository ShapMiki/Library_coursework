from sqlalchemy import insert, select
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

    @classmethod
    async def get_id_by_name(cls, name: str):
        async with async_session_maker() as session:
            query = select(cls.model.id).filter_by(name=name)
            result = await session.execute(query)
            return result.scalar_one_or_none()