from sqlalchemy import create_engine, text
from connection_string import connection_str


def delete_copy(copy_id):

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        transaction = connection.begin()

        try:

            # Get the book_id of the copy
            book_id = connection.execute(
                text("""
                    SELECT book_id
                    FROM copies
                    WHERE copy_id = :copy_id
                """),
                {
                    "copy_id": copy_id
                }
            ).scalar()

            if book_id is None:
                transaction.rollback()
                return "not_found"


            # Check for an open loan
            has_loans = connection.execute(
                text("""
                    SELECT loan_id
                    FROM loans
                    WHERE copy_id = :copy_id
                    LIMIT 1
                """),
                {"copy_id": copy_id}
            ).scalar()

            if has_loans is not None:
                transaction.rollback()
                return "has_loans"


            # Check how many other copies this book has
            other_copies = connection.execute(
                text("""
                    SELECT COUNT(*)
                    FROM copies
                    WHERE book_id = :book_id
                      AND copy_id <> :copy_id
                """),
                {
                    "book_id": book_id,
                    "copy_id": copy_id
                }
            ).scalar()


            # Delete the copy
            connection.execute(
                text("""
                    DELETE FROM copies
                    WHERE copy_id = :copy_id
                """),
                {
                    "copy_id": copy_id
                }
            )


            # If this was the last copy, delete the book
            if other_copies == 0:

                connection.execute(
                    text("""
                        DELETE FROM books
                        WHERE book_id = :book_id
                    """),
                    {
                        "book_id": book_id
                    }
                )

                transaction.commit()

                return "copy_and_book_deleted"


            transaction.commit()

            return "copy_deleted"


        except:

            transaction.rollback()
            raise