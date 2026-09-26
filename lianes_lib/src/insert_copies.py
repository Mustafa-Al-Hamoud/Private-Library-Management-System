from sqlalchemy import create_engine, text
from connection_string import connection_str
from datetime import date


def select_book_id():

    select_book = """
        SELECT MAX(book_id)
        FROM books;
    """

    engine = create_engine(connection_str())

    with engine.connect() as connection:
        bookID = connection.execute(
            text(select_book)
        ).scalar()

    return bookID

def insert_copy( price, copy_status):
    b_id = select_book_id()
    insert_copy_sql = """
        INSERT INTO copies
        (book_id, copy_status, purchase_price, purchase_date)
        VALUES (:book_id, :copy_status, :price, :purchase_date)
    """

    engine = create_engine(connection_str())

    with engine.connect() as connection:
        transaction = connection.begin()

        try:
            connection.execute(
                text(insert_copy_sql),
                {
                    "book_id": b_id,
                    "copy_status": copy_status,
                    "price": price,
                    "purchase_date": date.today()
                }
            )

            transaction.commit()

        except:
            transaction.rollback()
            raise