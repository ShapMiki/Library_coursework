from sqlalchemy import select, insert, update
from sqlalchemy.orm import selectinload
from datetime import date
from decimal import Decimal

from basedao.dao import BaseDAO
from database import async_session_maker

from user.model import User



class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_by_id(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update_one(cls, id, **kwargs):
        async with async_session_maker() as session:
            query = cls.model.__table__.update().values(**kwargs).where(cls.model.id == id)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def add_one(email: str, password: str, username: str):
        async with async_session_maker() as session:
            new_user = User(
                username=username,
                email=email,
                password=password,
            )
            session.add(new_user)
            await session.flush()

            await session.commit()
            await session.refresh(new_user)

            return new_user


