from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime


# Создание объекта MetaData, где ORM хранит информацию о схеме БД.
metadata = MetaData()


city = Table(
    'city',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False, unique=True),
)

zipcode = Table(
    'zipcode',
    metadata,
    Column('zip_code', Integer, primary_key=True),
    Column('city_id', ForeignKey('city.id', ondelete='CASCADE'), nullable=False),
)

account = Table(
    'account',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('email', String, nullable=False, unique=True),
    Column('password', String, nullable=False),
)

seller = Table(
    'seller',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('account_id', ForeignKey('account.id', ondelete='CASCADE'), nullable=False),
    Column('zip_code', ForeignKey('zipcode.zip_code'), nullable=False),
    Column('street', String, nullable=False),
    Column('home', String, nullable=False),
    Column('phone', String, nullable=False),
)

car = Table(
    'car',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('make', String, nullable=False),
    Column('model', String, nullable=False),
    Column('mileage', Integer, nullable=False),
    Column('num_owners', Integer, nullable=False, server_default=text('1')),
    Column('reg_number', String, nullable=False),
)

color = Table(
    'color',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False, unique=True),
    Column('hex', String, nullable=False, unique=True),
)

carcolor = Table(
    'carcolor',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('car_id', ForeignKey('car.id', ondelete='CASCADE'), nullable=False),
    Column('color_id', ForeignKey('color.id', ondelete='CASCADE'), nullable=False),
)

ad = Table(
    'ad',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('seller_id', ForeignKey('seller.id', ondelete='CASCADE'), nullable=False),
    Column('car_id', ForeignKey('car.id'), nullable=False),
    Column('title', String, nullable=False),
    Column('date', DateTime, nullable=False),
)


if __name__ == '__main__':
    # Создание таблиц в базе данных на основе описанной схемы.
    engine = create_engine('sqlite:///database1.sqlite', echo=True, future=True)
    metadata.create_all(engine)
