from sqlalchemy import select, insert, update, asc, desc
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
            query = (
                select(cls.model)
                .options(
                    selectinload(cls.model.author),
                    selectinload(cls.model.genre)
                )
            )
            result = await session.execute(query)
            books = result.scalars().all()
            return [book.to_dict() for book in books]

    @classmethod
    async def delete_by_id(cls, book_id: int):
        async with async_session_maker() as session:
            # Находим книгу
            book = await session.get(cls.model, book_id)
            if book:
                await session.delete(book)
                await session.commit()
                return True
            return False

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

            try:
                if "author_id" in book_data:
                    book.author_id = int(book_data["author_id"])

                if "genre_id" in book_data:
                    book.genre_id = int(book_data["genre_id"])
            except TypeError:
                pass

            if "extra_data" in book_data:

                if not book.extra_data:
                    book.extra_data = {}

                book.extra_data.update(book_data["extra_data"])

            await session.commit()
            await session.refresh(book)

            return book

    @classmethod
    async def find_filtered(cls, title: str = None, genre_id: int = None, author_id: int = None, sort_by: str = "title",
                            order: str = "asc"):
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.author), selectinload(cls.model.genre))

            if title:
                query = query.filter(cls.model.title.ilike(f"%{title}%"))

            if genre_id:
                query = query.filter(cls.model.genre_id == genre_id)

            if author_id:
                query = query.filter(cls.model.author_id == author_id)

            column = getattr(cls.model, sort_by, cls.model.title)
            if order == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))

            result = await session.execute(query)
            books = result.scalars().all()

            return [book.to_dict() for book in books]