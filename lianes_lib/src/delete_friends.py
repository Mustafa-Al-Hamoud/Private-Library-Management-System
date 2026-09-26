from sqlalchemy import create_engine, text

from connection_string import connection_str


def delete_friend(friend_id):

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

            has_loans = connection.execute(
                text("""
                    SELECT loan_id
                    FROM loans
                    WHERE friend_id = :friend_id
                    LIMIT 1
                """),
                {
                    "friend_id": friend_id
                }
            ).scalar()

            if has_loans is not None:
                transaction.rollback()
                return "has_loans"

            connection.execute(
                text("""
                
                    DELETE FROM friends
                    WHERE friend_id = :friend_id
                """),
                {
                    "friend_id": friend_id
                }
            )

            transaction.commit()
            return "deleted"

        except:

            transaction.rollback()
            raise