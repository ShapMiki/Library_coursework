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
            # author_data — это Pydantic-схема (SAuthor)
            orm_author = Author(name=author_data.name)
            session.add(orm_author)
            await session.commit()
            await session.refresh(orm_author)
            return orm_author
