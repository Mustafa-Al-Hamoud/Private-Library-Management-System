import pandas as pd
from sqlalchemy import create_engine, text

from connection_string import connection_str


def load_friends():

    friends_df = None

    select_friends = """
        SELECT
            friend_id,
            f_name,
            l_name,
            email,
            phone,
            adress,
            max_loans,
            is_trusted
        FROM friends
        ORDER BY friend_id DESC;
    """

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        transaction = connection.begin()

        try:

            friends_df = pd.DataFrame(
                connection.execute(
                    text(select_friends)
                )
            )

            transaction.commit()

        except:

            transaction.rollback()
            raise

    return friends_df