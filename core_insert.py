from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import insert

from core_schema import account
from core_schema import seller
from core_schema import car
from core_schema import color
from core_schema import carcolor
from core_schema import ad
from core_schema import city
from core_schema import zipcode


engine = create_engine('sqlite:///database1.sqlite', echo=True, future=True)


with engine.begin() as connection:
    connection.execute(
        insert(city),
        [
            {'name': 'Челябинск'},
            {'name': 'Москва'},
            {'name': 'Владивосток'},
        ],
    )

    connection.execute(
        insert(zipcode),
        [
            {'zip_code': 454000, 'city_id': 1},
            {'zip_code': 101000, 'city_id': 2},
            {'zip_code': 690000, 'city_id': 3},
        ],
    )

    connection.execute(
        insert(account),
        [
            {
                'first_name': 'Евгений',
                'last_name': 'Разгуляев',
                'email': 'box-1@mail.ru',
                'password': 'secret-password',
            },
            {
                'first_name': 'Алекс',
                'last_name': 'Миллер',
                'email': 'box-2@mail.ru',
                'password': 'secret-password',
            },
            {
                'first_name': 'Иван',
                'last_name': 'Семенов',
                'email': 'box-3@mail.ru',
                'password': 'secret-password',
            },
            {
                'first_name': 'Алена',
                'last_name': 'Петрова',
                'email': 'box-4@mail.ru',
                'password': 'secret-password',
            },
        ],
    )

    connection.execute(
        insert(seller),
        [
            {
                'account_id': 1,
                'zip_code': 454000,
                'street': 'Раздольная',
                'home': '5/A',
                'phone': '86541237845',
            },
            {
                'account_id': 3,
                'zip_code': 101000,
                'street': 'Ленина',
                'home': '125',
                'phone': '89198971212',
            },
        ],
    )

    connection.execute(
        insert(color),
        [
            {'name': 'красный', 'hex': 'ff0000'},
            {'name': 'синий', 'hex': '000066'},
            {'name': 'зеленый', 'hex': '339966'},
            {'name': 'желтый', 'hex': 'FFFF00'},
            {'name': 'черный', 'hex': '000000'},
        ],
    )

    connection.execute(
        insert(car),
        [
            {
                'make': 'Nissan',
                'model': 'Patrol',
                'mileage': 40500,
                'num_owners': 5,
                'reg_number': 'o423oo',
            },
            {
                'make': 'Mercedes',
                'model': 'GLA',
                'mileage': 5000,
                'num_owners': 1,
                'reg_number': 'x666xx',
            },
            {
                'make': 'ВАЗ',
                'model': '2110',
                'mileage': 10000,
                'num_owners': 2,
                'reg_number': 'м123ск',
            },
            {
                'make': 'УАЗ',
                'model': 'Patriot',
                'mileage': 25550,
                'num_owners': 3,
                'reg_number': 'п564оп',
            },
            {
                'make': 'Ford',
                'model': 'GT',
                'mileage': 100000,
                'num_owners': 4,
                'reg_number': 'к013ар',
            },
            {
                'make': 'Chevrolet',
                'model': 'Impala 1965',
                'mileage': 150000,
                'num_owners': 2,
                'reg_number': 'и555мп',
            },
        ],
    )

    connection.execute(
        insert(carcolor),
        [
            {'color_id': 1, 'car_id': 1},
            {'color_id': 2, 'car_id': 1},
            {'color_id': 3, 'car_id': 1},
            {'color_id': 1, 'car_id': 2},
            {'color_id': 2, 'car_id': 3},
            {'color_id': 2, 'car_id': 4},
            {'color_id': 3, 'car_id': 4},
        ]
    )

    connection.execute(
        insert(ad),
        [
            {
                'title': 'Продам внедорожник',
                'date': datetime(2019, 12, 1),
                'car_id': 1,
                'seller_id': 1,
            },
            {
                'title': 'Продам внедорожник с пробегом',
                'date': datetime(2020, 1, 1, 12, 0, 0),
                'car_id': 1,
                'seller_id': 1,
            },
            {
                'title': 'Продам мерседес после восстановления',
                'date': datetime(2012, 1, 15),
                'car_id': 2,
                'seller_id': 2,
            },
            {
                'title': 'Десятка в хорошем состоянии',
                'date': datetime(2018, 2, 27),
                'car_id': 3,
                'seller_id': 2,
            },
            {
                'title': 'Уаз в люкс комплектации',
                'date': datetime(2020, 3, 13),
                'car_id': 4,
                'seller_id': 2,
            },
        ],
    )
