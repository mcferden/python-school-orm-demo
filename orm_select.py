from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

from orm_schema import Ad
from orm_schema import Car
from orm_schema import Seller


engine = create_engine('sqlite:///database2.sqlite', echo=True, future=True)
Session = sessionmaker(engine, future=True)


def example1():
    with Session() as session:
        result = session.execute(
            select(Car)
            .where(Car.make == 'Nissan')
        )
        pprint(result.scalars().all())


def example2():
    """Пример фильтрации по атрибутам связанной сущности, используя join."""

    with Session() as session:
        result = session.execute(
            select(Ad)
            .join_from(Ad, Car)
            .where(Car.make == 'Nissan')
        )
        pprint(result.scalars().all())


def example3():
    """Пример фильтрации по атрибутам связанной сущности, используя метод has у relationship."""

    with Session() as session:
        result = session.execute(
            select(Ad)
            .where(Ad.car.has(make='Nissan'))
        )
        pprint(result.scalars().all())


def example4():
    """Пример группировки и использования агрегирующих функций на связанных таблицах через join.
    Задача: выбрать продавцов, публиковавших больше одного объявления."""

    with Session() as session:
        result = session.execute(
            select(Seller)
            .join_from(Seller, Ad)
            .group_by(Seller.id)
            .having(func.count(Ad.id) > 1)
        )
        pprint(result.scalars().all())


def example5():
    """Пример группировки и использования агрегирующих функций на связанных таблицах через подзапрос.
    Задача: выбрать продавцов, публиковавших больше одного объявления."""

    with Session() as session:
        result = session.execute(
            select(Seller)
            .where(Seller.id.in_(
                select(Ad.seller_id)
                .group_by(Ad.seller_id)
                .having(func.count(Ad.id) > 1)
            ))
        )
        pprint(result.scalars().all())


def example6():
    """Пример "жадной" загрузки связанных one to one сущностей через join.
    Выгружаем продавцов вместе с их аккаунтами."""

    with Session() as session:
        result = session.execute(
            select(Seller)
            .options(joinedload(Seller.account, innerjoin=True))
        )
        pprint(result.scalars().all())


def example7():
    with Session() as session:
        result = session.execute(
            select(Seller)
        )
        pprint(result.scalars().all())


def example8():
    """Пример "жадной" загрузки связанных one to many сущностей через select in.
    Выгружаем продавцов вместе с их объявлениями."""

    with Session() as session:
        result = session.execute(
            select(Seller)
            .options(
                joinedload(Seller.account, innerjoin=True),
                selectinload(Seller.ads),
            )
        )
        for seller in result.scalars():
            pprint(seller)
            pprint(seller.ads)


if __name__ == '__main__':
    # example1()
    # example2()
    # example3()
    # example4()
    # example5()
    # example6()
    example7()
    # example8()
