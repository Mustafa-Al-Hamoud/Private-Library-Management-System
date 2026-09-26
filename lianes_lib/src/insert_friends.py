from sqlalchemy import create_engine, text

from connection_string import connection_str


def insert_friend(
    f_name,
    l_name,
    email,
    phone,
    adress,
    max_loans,
    is_trusted,
    friend_notes
):

    insert_friend_sql = """
        INSERT INTO friends
        (
            f_name,
            l_name,
            email,
            phone,
            adress,
            max_loans,
            is_trusted,
            friend_notes
        )
        VALUES
        (
            :f_name,
            :l_name,
            :email,
            :phone,
            :adress,
            :max_loans,
            :is_trusted,
            :friend_notes
        )
    """

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        transaction = connection.begin()

        try:

            connection.execute(
                text(insert_friend_sql),
                {
                    "f_name": f_name,
                    "l_name": l_name,
                    "email": email,
                    "phone": phone,
                    "adress": adress,
                    "max_loans": max_loans,
                    "is_trusted": is_trusted,
                    "friend_notes": friend_notes
                }
            )

            transaction.commit()

        except:

            transaction.rollback()
            raise