from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload

from basedao.dao import BaseDAO
from database import async_session_maker

from book.model import Book



class BookDAO(BaseDAO):
    model = Book

    @classmethod
    async def add_one(cls, book_data):
        async with async_session_maker() as session:
            orm_book = Book(**book_data.dict())
            session.add(orm_book)
            await session.commit()
            await session.refresh(orm_book)
            return orm_book

    @classmethod
    async def update_one(cls, book_data):  # Исправлено
        async with async_session_maker() as session:
            # Находим книгу в той же сессии
            book = await session.get(Book, book_data["id"])

            if not book:
                return None

            # Обновляем поля
            book.title = book_data["title"]
            book.description = book_data["description"]

            # Если есть другие поля, обновляем и их
            if "author_id" in book_data:
                book.author_id = book_data["author_id"]
            if "genre_id" in book_data:
                book.genre_id = book_data["genre_id"]

            # Сохраняем изменения
            await session.commit()
            await session.refresh(book)

            return book