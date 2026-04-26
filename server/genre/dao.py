from sqlalchemy import insert, select
from basedao.dao import BaseDAO
from database import async_session_maker
from genre.model import Genre


class GenreDAO(BaseDAO):
    model = Genre

    @classmethod
    async def add_one(cls, genre_data):
        async with async_session_maker() as session:
            # Поддержка как объектов со свойством name, так и словарей
            name = genre_data.name if hasattr(genre_data, "name") else genre_data.get("name")
            orm_genre = Genre(name=name)
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

    @classmethod
    async def update_one(cls, genre_data):
        """
        Обновляет название жанра по его ID.
        Поддерживает формат списка (как в твоих формах редактирования книг).
        """
        async with async_session_maker() as session:
            # Если пришел список объектов (как из формы редактирования), берем первый
            data = genre_data[0] if isinstance(genre_data, list) else genre_data

            try:
                genre_id = int(data.get("id"))
                genre = await session.get(cls.model, genre_id)
            except (TypeError, ValueError):
                return None

            if not genre:
                return None

            if "name" in data:
                genre.name = data["name"]

            await session.commit()
            await session.refresh(genre)
            return genre

    @classmethod
    async def delete_by_id(cls, genre_id: int):
        """
        Удаляет жанр по ID. При удалении сработают триггеры в БД.
        """
        async with async_session_maker() as session:
            genre = await session.get(cls.model, genre_id)
            if genre:
                await session.delete(genre)
                await session.commit()
                return True
            return False