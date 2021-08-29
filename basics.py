from sqlalchemy import create_engine
from sqlalchemy import text


engine = create_engine('sqlite://', echo=True, future=True)


def example1():
    """Пример подключения к базе данных и выполнение простейшего запроса."""

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 'Hello, world!'"))
        print(result.scalar_one())


def example2():
    """Пример создания таблицы и записи данных. Демонстрация что при использовании engine.connect
    в конце контекстного менеджера происходит ROLLBACK."""

    with engine.connect() as connection:
        connection.execute(
            text("CREATE TABLE example (x INTEGER, y INTEGER)"),
        )
        connection.execute(
            text("INSERT INTO example (x, y) VALUES (:x, :y)"),
            [{'x': 1, 'y': 1}, {'x': 2, 'y': 4}],
        )

    with engine.connect() as connection:
        result = connection.execute(text("SELECT x, y FROM example"))
        print(result.all())


def example3():
    """Пример явного использования commit и engine.connect."""

    with engine.connect() as connection:
        connection.execute(
            text("CREATE TABLE example (x INTEGER, y INTEGER)"),
        )
        connection.execute(
            text("INSERT INTO example (x, y) VALUES (:x, :y)"),
            [{'x': 1, 'y': 1}, {'x': 2, 'y': 4}],
        )
        connection.commit()

    with engine.connect() as connection:
        result = connection.execute(text("SELECT x, y FROM example"))
        print(result.all())


def example4():
    """Пример неявного использования commit и engine.begin."""

    with engine.begin() as connection:
        connection.execute(
            text("CREATE TABLE example (x INTEGER, y INTEGER)"),
        )
        connection.execute(
            text("INSERT INTO example (x, y) VALUES (:x, :y)"),
            [{'x': 1, 'y': 1}, {'x': 2, 'y': 4}],
        )

    with engine.connect() as connection:
        result = connection.execute(text("SELECT x, y FROM example"))
        print(result.all())


if __name__ == '__main__':
    example1()
    # example2()
    # example3()
    # example4()
