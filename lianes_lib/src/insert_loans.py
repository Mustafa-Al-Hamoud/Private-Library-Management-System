from sqlalchemy import create_engine, text

from connection_string import connection_str


def insert_loan(copy_id, friend_id, confirmed=False):

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        transaction = connection.begin()

        try:

            # ─────────────────────────────────
            # Check Copy
            # ─────────────────────────────────

            copy_status = connection.execute(
                text("""
                    SELECT copy_status
                    FROM copies
                    WHERE copy_id = :copy_id
                """),
                {
                    "copy_id": copy_id
                }
            ).scalar()

            if copy_status is None:

                transaction.rollback()
                return "copy_not_found"

            if copy_status != "Available":

                transaction.rollback()
                return "copy_not_available"


            # ─────────────────────────────────
            # Check Friend
            # ─────────────────────────────────

            friend_data = connection.execute(
                text("""
                    SELECT
                        max_loans,
                        is_trusted
                    FROM friends
                    WHERE friend_id = :friend_id
                """),
                {
                    "friend_id": friend_id
                }
            ).mappings().first()

            if friend_data is None:

                transaction.rollback()
                return "friend_not_found"


            # ─────────────────────────────────
            # Check Trusted Status
            # ─────────────────────────────────

            if not friend_data["is_trusted"] and not confirmed:

                transaction.rollback()
                return "friend_not_trusted"


            # ─────────────────────────────────
            # Check Maximum Loans
            # ─────────────────────────────────

            current_loans = connection.execute(
                text("""
                    SELECT COUNT(*)
                    FROM loans
                    WHERE friend_id = :friend_id
                      AND return_date IS NULL
                """),
                {
                    "friend_id": friend_id
                }
            ).scalar()

            if current_loans >= friend_data["max_loans"] and not confirmed:
                transaction.rollback()
                return "max_loans_reached"


            # ─────────────────────────────────
            # Create Loan
            # ─────────────────────────────────

            connection.execute(
                text("""
                    INSERT INTO loans
                    (
                        copy_id,
                        friend_id
                    )
                    VALUES
                    (
                        :copy_id,
                        :friend_id
                    )
                """),
                {
                    "copy_id": copy_id,
                    "friend_id": friend_id
                }
            )


            # ─────────────────────────────────
            # Change Copy Status
            # ─────────────────────────────────

            connection.execute(
                text("""
                    UPDATE copies
                    SET copy_status = 'Borrowed'
                    WHERE copy_id = :copy_id
                """),
                {
                    "copy_id": copy_id
                }
            )


            transaction.commit()

            return "created"


        except:

            transaction.rollback()
            raise