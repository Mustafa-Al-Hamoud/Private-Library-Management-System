from sqlalchemy import create_engine, text
from connection_string import connection_str


def get_copy_details(copy_id):

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    c.copy_id,
                    c.book_id,
                    c.copy_status,
                    c.purchase_price,
                    c.purchase_date,
                    b.title,
                    b.author,
                    b.genre,
                    b.isbn,
                    b.publicationyear
                FROM copies c
                INNER JOIN books b
                    ON c.book_id = b.book_id
                WHERE c.copy_id = :copy_id
            """),
            {
                "copy_id": copy_id
            }
        ).mappings().first()

    return result

def update_copy(
    copy_id,
    title,
    author,
    genre,
    isbn,
    publicationyear,
    copy_status,
    purchase_price,
    purchase_date
):

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        transaction = connection.begin()

        try:

            # Get the book_id belonging to this copy
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


            # Update Book
            connection.execute(
                text("""
                    UPDATE books
                    SET
                        title = :title,
                        author = :author,
                        genre = :genre,
                        isbn = :isbn,
                        publicationyear = :publicationyear
                    WHERE book_id = :book_id
                """),
                {
                    "title": title,
                    "author": author,
                    "genre": genre,
                    "isbn": isbn,
                    "publicationyear": publicationyear,
                    "book_id": book_id
                }
            )


            # Update Copy
            connection.execute(
                text("""
                    UPDATE copies
                    SET
                        copy_status = :copy_status,
                        purchase_price = :purchase_price,
                        purchase_date = :purchase_date
                    WHERE copy_id = :copy_id
                """),
                {
                    "copy_status": copy_status,
                    "purchase_price": purchase_price,
                    "purchase_date": purchase_date,
                    "copy_id": copy_id
                }
            )


            transaction.commit()

            return "updated"


        except:

            transaction.rollback()
            raise