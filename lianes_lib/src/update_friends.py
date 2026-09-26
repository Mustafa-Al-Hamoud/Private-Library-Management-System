from sqlalchemy import create_engine, text

from connection_string import connection_str


def get_friend_details(friend_id):

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    friend_id,
                    f_name,
                    l_name,
                    email,
                    phone,
                    adress,
                    max_loans,
                    is_trusted,
                    friend_notes
                FROM friends
                WHERE friend_id = :friend_id
            """),
            {
                "friend_id": friend_id
            }
        ).mappings().first()

    return result


def update_friend(
    friend_id,
    f_name,
    l_name,
    email,
    phone,
    adress,
    max_loans,
    is_trusted,
    friend_notes
):

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        transaction = connection.begin()

        try:

            friend_exists = connection.execute(
                text("""
                    SELECT friend_id
                    FROM friends
                    WHERE friend_id = :friend_id
                """),
                {
                    "friend_id": friend_id
                }
            ).scalar()

            if friend_exists is None:
                transaction.rollback()
                return "not_found"

            connection.execute(
                text("""
                    UPDATE friends
                    SET
                        f_name = :f_name,
                        l_name = :l_name,
                        email = :email,
                        phone = :phone,
                        adress = :adress,
                        max_loans = :max_loans,
                        is_trusted = :is_trusted,
                        friend_notes = :friend_notes
                    WHERE friend_id = :friend_id
                """),
                {
                    "f_name": f_name,
                    "l_name": l_name,
                    "email": email,
                    "phone": phone,
                    "adress": adress,
                    "max_loans": max_loans,
                    "is_trusted": is_trusted,
                    "friend_notes": friend_notes,
                    "friend_id": friend_id
                }
            )

            transaction.commit()
            return "updated"

        except:

            transaction.rollback()
            raise