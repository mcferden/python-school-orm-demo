from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    zip_codes = relationship('ZipCode', back_populates='city')


class ZipCode(Base):
    __tablename__ = 'zipcode'

    zip_code = Column(Integer, primary_key=True)
    city_id = Column(ForeignKey('city.id', ondelete='CASCADE'), nullable=False)

    city = relationship('City', back_populates='zip_codes')


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    # Параметр uselist=False указывает на то, что отношение one to one.
    seller = relationship('Seller', back_populates='account', uselist=False)


class Seller(Base):
    __tablename__ = 'seller'

    id = Column(Integer, primary_key=True)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    zip_code = Column(ForeignKey('zipcode.zip_code'), nullable=False)
    street = Column(String, nullable=False)
    home = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    # Параметры lazy='joined' и innerjoin=True указывают, что при выгрузке объектов seller,
    # нужно так же одновременно выгружать связанный объект account, используя inner join.
    account = relationship('Account', back_populates='seller', lazy='joined', innerjoin=True)
    ads = relationship('Ad', back_populates='seller')

    def __repr__(self):
        return f'Seller(first_name={self.account.first_name}, last_name={self.account.last_name})'


carcolor = Table(
    'carcolor',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('car_id', ForeignKey('car.id', ondelete='CASCADE'), nullable=False),
    Column('color_id', ForeignKey('color.id', ondelete='CASCADE'), nullable=False),
)


class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    mileage = Column(Integer, nullable=False)
    num_owners = Column(Integer, nullable=False, server_default=text('1'))
    reg_number = Column(String, nullable=False)

    colors = relationship('Color', secondary=carcolor)
    ads = relationship('Ad', back_populates='car')

    def __repr__(self):
        return f'Car(make={self.make}, model={self.model})'


class Color(Base):
    __tablename__ = 'color'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    hex = Column(String, nullable=False, unique=True)


class Ad(Base):
    __tablename__ = 'ad'

    id = Column(Integer, primary_key=True)
    seller_id = Column(ForeignKey('seller.id', ondelete='CASCADE'), nullable=False)
    car_id = Column(ForeignKey('car.id'), nullable=False)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

    seller = relationship('Seller', back_populates='ads')
    car = relationship('Car', back_populates='ads')

    def __repr__(self):
        return f'Ad(title={self.title}, date={self.date})'


if __name__ == '__main__':
    engine = create_engine('sqlite:///database2.sqlite', echo=True, future=True)
    Base.metadata.create_all(engine)
