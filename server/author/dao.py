from sqlalchemy import select, insert, update, asc, desc
from sqlalchemy.orm import selectinload

from basedao.dao import BaseDAO
from database import async_session_maker

from author.model import Author


class AuthorDAO(BaseDAO):
    model = Author

    @classmethod
    async def add_one(cls, author_data):
        async with async_session_maker() as session:
            # Поддержка как объектов Pydantic, так и словарей
            name = author_data.name if hasattr(author_data, "name") else author_data.get("name")
            orm_author = Author(name=name)
            session.add(orm_author)
            await session.commit()
            await session.refresh(orm_author)
            return orm_author

    @classmethod
    async def update_one(cls, author_data):
        """
        Обновляет данные автора. Принимает либо словарь, либо список со словарем.
        """
        async with async_session_maker() as session:
            data = author_data[0] if isinstance(author_data, list) else author_data

            try:
                author_id = int(data.get("id"))
                author = await session.get(cls.model, author_id)
            except (TypeError, ValueError):
                return None

            if not author:
                return None

            if "name" in data:
                author.name = data["name"]

            await session.commit()
            await session.refresh(author)
            return author

    @classmethod
    async def delete_by_id(cls, author_id: int):
        """
        Удаляет автора по ID.
        """
        async with async_session_maker() as session:
            author = await session.get(cls.model, author_id)
            if author:
                await session.delete(author)
                await session.commit()
                return True
            return False