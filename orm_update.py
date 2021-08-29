from datetime import datetime
from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import selectinload

from orm_schema import Ad
from orm_schema import Car
from orm_schema import Seller


engine = create_engine('sqlite:///database2.sqlite', echo=True, future=True)
Session = sessionmaker(engine, future=True)


def example1():
    """При повторной выборке объекта с таким же id возвращается один и тот же объект."""

    with Session() as session:
        seller1 = session.execute(
            select(Seller)
            .where(Seller.id == 1)
        ).scalar_one()

        seller2 = session.execute(
            select(Seller)
            .where(Seller.id == 1)
        ).scalar_one()

        print(seller1 is seller2)


def example2():
    """Пример изменения поля через ORM."""

    with Session() as session:
        seller = session.execute(
            select(Seller)
            .where(Seller.id == 1)
        ).scalar_one()

        print(seller.home)
        seller.home = '13'
        session.commit()
        print(seller.home)


def example3():
    """При повторной выборке объекта с таким же id возвращается один и тот же объект.
    Пример, как это можно использовать при обновлении одного объекта в нескольких местах."""

    with Session() as session:
        seller1 = session.execute(
            select(Seller)
            .where(Seller.id == 2)
        ).scalar_one()

        print(seller1)
        seller1.account.first_name = 'Петр'
        print(seller1)

        seller2 = session.execute(
            select(Seller)
            .where(Seller.id == 2)
        ).scalar_one()

        print(seller2)
        seller2.account.last_name = 'Иванов'
        print(seller2)

        session.commit()

        print(seller1)
        print(seller2)


def example4():
    """Редактирование коллекций связанных сущностей.
    Задача: опубликовать новое объявление."""

    with Session() as session:
        seller = session.execute(
            select(Seller)
            .where(Seller.id == 1)
            .options(selectinload(Seller.ads))
        ).scalar_one()

        car = Car(
            make='Kia',
            model='Stinger',
            mileage=5000,
            reg_number='с321тн',
        )

        ad = Ad(
            seller=seller,
            car=car,
            title='Продам Kia Stinger',
            date=datetime(2021, 2, 1),
        )

        pprint(seller.ads)

        seller.ads.append(ad)
        session.commit()

        pprint(seller.ads)


if __name__ == '__main__':
    example1()
    # example2()
    # example3()
    # example4()
