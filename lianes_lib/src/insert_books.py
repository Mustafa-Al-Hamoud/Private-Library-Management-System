from sqlalchemy import create_engine, text
from connection_string import connection_str


def insert_book(t_value, a_value, g_value, i_value, p_value):

    insert_book = """
        INSERT INTO books
        (title, author, genre, isbn, publicationyear)
        VALUES (:title, :author, :genre, :isbn, :publicationyear)
    """

    engine = create_engine(connection_str())

    with engine.connect() as connection:
        transaction = connection.begin()

        try:
            connection.execute(
                text(insert_book),
                {
                    "title": t_value,
                    "author": a_value,
                    "genre": g_value,
                    "isbn": i_value,
                    "publicationyear": p_value
                }
            )

            transaction.commit()

        except:
            transaction.rollback()
            raise