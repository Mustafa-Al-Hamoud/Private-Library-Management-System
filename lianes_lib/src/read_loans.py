import pandas as pd
from sqlalchemy import create_engine, text

from connection_string import connection_str


def load_loans():

    loans_df = None

    select_loans = """
        SELECT
            l.loan_id,
            l.copy_id,
            b.title,
            l.friend_id,
            f.f_name,
            f.l_name,
            l.loan_date,
            l.due_date,
            l.return_date,
            c.copy_status
        FROM loans l

        INNER JOIN copies c
            ON l.copy_id = c.copy_id

        INNER JOIN books b
            ON c.book_id = b.book_id

        INNER JOIN friends f
            ON l.friend_id = f.friend_id

        ORDER BY l.loan_id DESC;
    """

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        transaction = connection.begin()

        try:

            loans_df = pd.DataFrame(
                connection.execute(
                    text(select_loans)
                )
            )

            transaction.commit()

        except:

            transaction.rollback()
            raise

    return loans_df