from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from orm_schema import Account
from orm_schema import Seller
from orm_schema import Car
from orm_schema import Color
from orm_schema import Ad
from orm_schema import City
from orm_schema import ZipCode


engine = create_engine('sqlite:///database2.sqlite', echo=True, future=True)


with Session(engine, future=True) as session:
    city1 = City(
        name='Челябинск',
        zip_codes=[ZipCode(zip_code=454000)],
    )
    city2 = City(
        name='Москва',
        zip_codes=[ZipCode(zip_code=101000)],
    )
    city3 = City(
        name='Владивосток',
        zip_codes=[ZipCode(zip_code=690000)],
    )

    account1 = Account(
        first_name='Евгений',
        last_name='Разгуляев',
        email='box-1@mail.ru',
        password='secret-password',
    )
    account2 = Account(
        first_name='Алекс',
        last_name='Миллер',
        email='box-2@mail.ru',
        password='secret-password',
    )
    account3 = Account(
        first_name='Иван',
        last_name='Семенов',
        email='box-3@mail.ru',
        password='secret-password',
    )
    account4 = Account(
        first_name='Алена',
        last_name='Петрова',
        email='box-4@mail.ru',
        password='secret-password',
    )

    seller1 = Seller(
        zip_code=454000,
        street='Раздольная',
        home='5/A',
        phone='86541237845',
        account=account1,
    )
    seller2 = Seller(
        zip_code=101000,
        street='Ленина',
        home='125',
        phone='89198971212',
        account=account3,
    )

    color1 = Color(name='красный', hex='ff0000')
    color2 = Color(name='синий', hex='000066')
    color3 = Color(name='зеленый', hex='339966')
    color4 = Color(name='желтый', hex='ffff00')
    color5 = Color(name='черный', hex='000000')

    car1 = Car(
        make='Nissan',
        model='Patrol',
        mileage=40500,
        num_owners=5,
        reg_number='o423oo',
        colors=[color1, color2, color3],
    )
    car2 = Car(
        make='Mercedes',
        model='GLA',
        mileage=5000,
        num_owners=1,
        reg_number='x666xx',
        colors=[color1],
    )
    car3 = Car(
        make='ВАЗ',
        model='2110',
        mileage=10000,
        num_owners=2,
        reg_number='м123ск',
        colors=[color2],
    )
    car4 = Car(
        make='УАЗ',
        model='Patriot',
        mileage=25550,
        num_owners=3,
        reg_number='п564оп',
        colors=[color2, color3],
    )
    car5 = Car(
        make='Ford',
        model='GT',
        mileage=100000,
        num_owners=4,
        reg_number='к013ар',
    )
    car6 = Car(
        make='Chevrolet',
        model='Impala 1965',
        mileage=150000,
        num_owners=2,
        reg_number='и555мп',
    )

    ad1 = Ad(
        title='Продам внедорожник',
        date=datetime(2019, 12, 1),
        car=car1,
        seller=seller1,
    )
    ad2 = Ad(
        title='Продам внедорожник с пробегом',
        date=datetime(2020, 1, 1, 12, 0, 0),
        car=car1,
        seller=seller1,
    )
    ad3 = Ad(
        title='Продам мерседес после восстановления',
        date=datetime(2012, 1, 15),
        car=car2,
        seller=seller2,
    )
    ad4 = Ad(
        title='Десятка в хорошем состоянии',
        date=datetime(2018, 2, 27),
        car=car3,
        seller=seller2,
    )
    ad5 = Ad(
        title='Уаз в люкс комплектации',
        date=datetime(2020, 3, 13),
        car=car4,
        seller=seller2,
    )

    # Добавляем все новые объекты в сессию. Порядок добавления значения не имеет.
    # Вместо add_all, можно добавлять объекты по одному через add.
    session.add_all([city1, city2, city3])
    session.add_all([account1, account2, account3, account4])
    session.add_all([color1, color2, color3, color4, color5])
    session.add_all([car1, car2, car3, car4, car5, car6])
    session.add_all([ad1, ad2, ad3, ad4, ad5])

    # Сохраняем результаты. Только в этот момент начинаю выполняться запросы.
    session.commit()
