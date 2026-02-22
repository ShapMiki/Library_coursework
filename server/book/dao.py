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

