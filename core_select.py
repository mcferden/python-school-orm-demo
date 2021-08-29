from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import literal_column
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy import and_

from core_schema import ad
from core_schema import car


engine = create_engine('sqlite:///database1.sqlite', echo=True, future=True)


def example1():
    """Пример выборки данных по условию: выбрать все автомобили производителей ВАЗ и УАЗ.
    Выбираются все колонки."""

    with engine.connect() as connection:
        result = connection.execute(
            select(car)
            .where(car.c.make.in_(['ВАЗ', 'УАЗ'])),
        )
        pprint(result.all())


def example2():
    """Пример выборки данных по условию: выбрать все автомобили производителей ВАЗ и УАЗ.
    Выбираются только колонки make и model."""

    with engine.connect() as connection:
        result = connection.execute(
            select(
                car.c.make,
                car.c.model,
            )
            .where(car.c.make.in_(['ВАЗ', 'УАЗ'])),
        )
        pprint(result.all())


def example3():
    """Пример выборки данных по условию равенства."""

    with engine.connect() as connection:
        result = connection.execute(
            select(car.c.model)
            .where(car.c.make == 'ВАЗ'),
        )
        pprint(result.all())


def example4():
    """Пример выборки данных по условию LIKE."""

    with engine.connect() as connection:
        result = connection.execute(
            select(
                car.c.make,
                car.c.model,
            )
            .where(car.c.make.like('%А%')),
        )
        pprint(result.all())


def example5():
    """Пример выборки значения вместо колонки таблицы."""

    with engine.connect() as connection:
        result = connection.execute(
            select(literal_column('1 + 1')),
        )
        pprint(result.scalar_one())


def example6():
    """Пример выборки не из таблицы, а из списка значений."""

    with engine.connect() as connection:
        result = connection.execute(
            select('*')
            .select_from(
                text("(VALUES ('Даша', 'Саша'), ('Бегемот', 'Бергамот')) AS pairs"),
            ),
        )
        pprint(result.all())


def example7():
    """Применение агрегирующих функций.
    Выбирается минимальный, средний и максимальный пробег среди всх автомобилей."""

    with engine.connect() as connection:
        result = connection.execute(
            select(
                func.min(car.c.mileage).label('min_mileage'),
                func.avg(car.c.mileage).label('avg_mileage'),
                func.max(car.c.mileage).label('max_mileage'),
            ),
        )
        pprint(result.one())


def example8():
    """Пример сортировки и ограничения количества выбираемых строк.
    Задача: выбрать автомобиль с наибольшим количеством владельцев."""

    with engine.connect() as connection:
        result = connection.execute(
            select(
                car.c.model,
                car.c.num_owners,
            )
            .order_by(car.c.num_owners.desc())
            .limit(1),
        )
        pprint(result.one())


def example9():
    """Пример использования подзапросов в условии выборки.
    Задача: выбрать производителей автомобилей у которых пробег больше среднего."""

    with engine.connect() as connection:
        result = connection.execute(
            select(car.c.make)
            .distinct()
            .where(car.c.mileage > (
                select(func.avg(car.c.mileage))
                .scalar_subquery()
            )),
        )
        pprint(result.all())


def example10():
    """Пример использования подзапросов с alias в условии выборки.
    Задача: вывести объявления, которые уже размещались ранее."""

    with engine.connect() as connection:
        prior_ad = ad.alias()
        result = connection.execute(
            select(
                ad.c.id,
                ad.c.title,
            )
            .where(
                select(func.count() > 0)
                .select_from(prior_ad)
                .where(
                    prior_ad.c.car_id == ad.c.car_id,
                    prior_ad.c.seller_id == ad.c.seller_id,
                    prior_ad.c.date < ad.c.date,
                )
                .scalar_subquery(),
            ),
        )
        pprint(result.all())


def example11():
    """Пример использования подзапросов с конструкцией exists в условии выборки.
    Задача: вывести объявления, которые уже размещались ранее."""

    with engine.connect() as connection:
        prior_ad = ad.alias()
        result = connection.execute(
            select(
                ad.c.id,
                ad.c.title,
            )
            .where(
                select(prior_ad.c.id)
                .select_from(prior_ad)
                .where(
                    prior_ad.c.car_id == ad.c.car_id,
                    prior_ad.c.seller_id == ad.c.seller_id,
                    prior_ad.c.date < ad.c.date,
                )
                .exists(),
            ),
        )
        pprint(result.all())


def example12():
    """Пример использования соединения для фильтрации строк.
    Задача: вывести объявления, которые уже размещались ранее."""

    with engine.connect() as connection:
        prior_ad = ad.alias()
        result = connection.execute(
            select(
                ad.c.id,
                ad.c.title,
            )
            .join_from(ad, prior_ad, and_(
                prior_ad.c.car_id == ad.c.car_id,
                prior_ad.c.seller_id == ad.c.seller_id,
                prior_ad.c.date < ad.c.date,
            )),
        )
        pprint(result.all())


def example13():
    """Пример использования подзапросов в select.
    Задача: для каждого автомобиля получить кол-во автомобилей с таким-же производителем."""

    with engine.connect() as connection:
        car_alias = car.alias()
        result = connection.execute(
            select(
                car.c.make,
                car.c.model,
                select(func.count(car_alias.c.id))
                .select_from(car_alias)
                .where(
                    car_alias.c.make == car.c.make,
                    car_alias.c.id != car.c.id,
                )
                .scalar_subquery(),
            ),
        )
        pprint(result.all())


def example14():
    """Пример использования оконных функций.
    Задача: вывести общее кол-во владельцев всех автомобилей вместе с каждых автомобилем."""

    with engine.connect() as connection:
        result = connection.execute(
            select(
                car.c.id,
                car.c.make,
                car.c.model,
                func.sum(car.c.num_owners).over(),
            )
        )
        pprint(result.all())


def example15():
    """Пример использования оконных функций с разбиением.
    Задача: вывести общее кол-во владельцев по каждому производителю вместе с каждых автомобилем."""

    with engine.connect() as connection:
        result = connection.execute(
            select(
                car.c.id,
                car.c.make,
                func.sum(car.c.num_owners).over(partition_by=car.c.make),
            ),
        )
        pprint(result.all())


def example16():
    """Пример использования оконных функций с упорядочиванием.
    Задача: вывести накопительную сумму владельцев в порядке id автомобилей."""

    with engine.connect() as connection:
        result = connection.execute(
            select(
                car.c.id,
                car.c.make,
                car.c.model,
                car.c.num_owners,
                func.sum(car.c.num_owners).over(order_by=car.c.id),
            ),
        )
        pprint(result.all())


def example17():
    """Пример оконной функции с упорядочиванием по нескольким колонкам."""

    with engine.connect() as connection:
        result = connection.execute(
            select(
                car.c.id,
                func.row_number().over(order_by=[car.c.make, car.c.num_owners]),
                car.c.make,
                car.c.num_owners,
            )
            .order_by(car.c.id),
        )
        pprint(result.all())


def example18():
    """Пример использования оконной функции row_number для решения задачи top N in groups.
    Задача: для каждого автопроизводителя вывести автомобиль с наибольшим кол-вом владельцев."""

    with engine.connect() as connection:
        subquery = select(
            car,
            func.row_number()
            .over(partition_by=car.c.make, order_by=car.c.num_owners.desc())
            .label('row_number'),
        ).subquery()

        result = connection.execute(
            select(
                subquery.c.id,
                subquery.c.make,
                subquery.c.model,
                subquery.c.num_owners,
            )
            .select_from(subquery)
            .where(subquery.c.row_number == 1)
        )

        pprint(result.all())


def example19():
    """Пример фильтрации в агрегирующих функциях."""

    with engine.connect() as connection:
        result = connection.execute(
            select(
                func.sum(car.c.num_owners),
                func.sum(car.c.num_owners).filter(car.c.make == 'Nissan'),
            )
        )
        pprint(result.one())


def example20():
    """Пример фильтрации в оконных функциях."""

    with engine.connect() as connection:
        result = connection.execute(
            select(
                func.sum(car.c.num_owners).over(partition_by=car.c.make),
                func.sum(car.c.num_owners).filter(car.c.make == 'Nissan').over(partition_by=car.c.make),
            )
        )
        pprint(result.all())


def example21():
    """Пример простого CTE.
    Задача: выбрать автомобили с пробегом больше среднего."""

    with engine.connect() as connection:
        avg_mileage = select(func.avg(car.c.mileage).label('value')).cte()
        result = connection.execute(
            select(car)
            .where(car.c.mileage > avg_mileage.c.value)
        )
        pprint(result.all())


def example22():
    """Пример использования нескольких CTE.
    Задача: выбрать производителей и кол-во моделей производителя тех автомобилей,
    у которых объявление публиковалось после 2020 года, а километраж выше среднего за тот же период."""

    with engine.connect() as connection:
        cars_from_2020 = (
            select(ad.c.car_id)
            .distinct()
            .where(ad.c.date > '2020-01-01')
            .cte()
        )
        avg_mileage = (
            select(func.avg(car.c.mileage).label('value'))
            .join_from(car, cars_from_2020, car.c.id == cars_from_2020.c.car_id)
            .cte()
        )
        result = connection.execute(
            select(
                car.c.make,
                func.count(car.c.model).over(partition_by=car.c.make)
            )
            .select_from(car, avg_mileage)
            .join(cars_from_2020, car.c.id == cars_from_2020.c.car_id)
            .where(car.c.mileage > avg_mileage.c.value)
        )
        pprint(result.all())


if __name__ == '__main__':
    example1()
    # example2()
    # example3()
    # example4()
    # example5()
    # example6()
    # example7()
    # example8()
    # example9()
    # example10()
    # example11()
    # example12()
    # example13()
    # example14()
    # example15()
    # example16()
    # example17()
    # example18()
    # example19()
    # example20()
    # example21()
    # example22()
