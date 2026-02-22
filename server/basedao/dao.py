from database import async_session_maker

from sqlalchemy import select, insert

class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_one(cls, model):
        async with async_session_maker() as session:
            session.add(model)
            await session.commit()



    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            cars = await session.execute(query)
            return cars.scalars().all()

    @classmethod
    async def find_by_id(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, obj):
        async with async_session_maker() as session:
            async with session.begin():
                session.add(obj)
                await session.commit()
                return obj

    @classmethod
    async def update(cls, obj):
        async with async_session_maker() as session:
            async with session.begin():
                session.merge(obj)
                await session.commit()
                return obj

    @classmethod
    async def delete(cls, obj):
        async with async_session_maker() as session:
            async with session.begin():
                session.delete(obj)
                await session.commit()
                return obj

    @classmethod
    async def delete_by_id(cls, id):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(id=id)
                result = await session.execute(query)
                obj = result.scalar_one_or_none()
                if obj:
                    await session.delete(obj)
                    await session.commit()
                return obj