from sqlalchemy import create_engine, text

from connection_string import connection_str


def update_loan(loan_id, copy_status):

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        transaction = connection.begin()

        try:

            # Check that the loan exists and is still open
            loan_data = connection.execute(
                text("""
                    SELECT
                        copy_id,
                        return_date
                    FROM loans
                    WHERE loan_id = :loan_id
                """),
                {
                    "loan_id": loan_id
                }
            ).mappings().first()

            if loan_data is None:
                transaction.rollback()
                return "not_found"

            if loan_data["return_date"] is not None:
                transaction.rollback()
                return "already_closed"


            # Close the loan
            connection.execute(
                text("""
                    UPDATE loans
                    SET return_date = CURRENT_DATE()
                    WHERE loan_id = :loan_id
                """),
                {
                    "loan_id": loan_id
                }
            )


            # Update copy status
            connection.execute(
                text("""
                    UPDATE copies
                    SET copy_status = :copy_status
                    WHERE copy_id = :copy_id
                """),
                {
                    "copy_status": copy_status,
                    "copy_id": loan_data["copy_id"]
                }
            )


            transaction.commit()

            return "updated"


        except:

            transaction.rollback()
            raise