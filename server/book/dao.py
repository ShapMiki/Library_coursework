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
    async def find_all_full(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            books = await session.execute(query)
            books = books.scalars().all()
            book_list = []
            for book in books:
                book_list.append(
                    {
                        "id": book.id,
                        "title": book.title,
                        "description": book.description,
                        "author_id": book.author_id,
                        "genre_id": book.genre_id,
                        "author": book.author.name if book.author else None,
                        "genre": book.genre.name if book.genre else None
                    }
                )
            return book_list

    @classmethod
    async def update_one(cls, book_data):

        async with async_session_maker() as session:

            try:
                book = await session.get(Book, int(book_data["id"]))
            except:
                return None

            if not book:
                return None

            if "title" in book_data:
                book.title = book_data["title"]

            if "description" in book_data:
                book.description = book_data["description"]

            if "author_id" in book_data:
                book.author_id = book_data["author_id"]

            if "genre_id" in book_data:
                book.genre_id = book_data["genre_id"]

            if "extra_data" in book_data:

                if not book.extra_data:
                    book.extra_data = {}

                book.extra_data.update(book_data["extra_data"])

            await session.commit()
            await session.refresh(book)

            return book
