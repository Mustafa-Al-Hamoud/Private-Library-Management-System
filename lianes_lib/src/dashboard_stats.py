from sqlalchemy import create_engine, text
from connection_string import connection_str


def get_book_statistics():

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        total_books = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM books
            """)
        ).scalar()

        status_counts = connection.execute(
            text("""
                SELECT
                    copy_status,
                    COUNT(*) AS count
                FROM copies
                GROUP BY copy_status
            """)
        ).mappings().all()

    status_dict = {
        "Available": 0,
        "Borrowed": 0,
        "Lost": 0,
        "Not available for borrowing": 0,
        "Worn out": 0
    }

    for row in status_counts:
        status_dict[row["copy_status"]] = row["count"]

    return total_books, status_dict

def get_loans_per_month(start_date, end_date):

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                WITH RECURSIVE months AS (
                    SELECT DATE_FORMAT(:start_date, '%Y-%m-01') AS month
                    UNION ALL
                    SELECT DATE_ADD(month, INTERVAL 1 MONTH)
                    FROM months
                    WHERE month < DATE_FORMAT(:end_date, '%Y-%m-01')
                )

                SELECT
                    DATE_FORMAT(months.month, '%Y-%m') AS month,
                    COUNT(loans.loan_id) AS loan_count
                FROM months
                LEFT JOIN loans
                    ON loans.loan_date >= months.month
                    AND loans.loan_date < DATE_ADD(months.month, INTERVAL 1 MONTH)
                    AND loans.loan_date BETWEEN :start_date AND :end_date
                GROUP BY months.month
                ORDER BY months.month
            """),
            {
                "start_date": start_date,
                "end_date": end_date
            }
        ).mappings().all()

    return result

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    DATE_FORMAT(loan_date, '%Y-%m') AS month,
                    COUNT(*) AS loan_count
                FROM loans
                WHERE loan_date BETWEEN :start_date AND :end_date
                GROUP BY DATE_FORMAT(loan_date, '%Y-%m')
                ORDER BY month
            """),
            {
                "start_date": start_date,
                "end_date": end_date
            }
        ).mappings().all()

    return result

def get_spending_per_month(start_date, end_date):

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                WITH RECURSIVE months AS (
                    SELECT DATE_FORMAT(:start_date, '%Y-%m-01') AS month
                    UNION ALL
                    SELECT DATE_ADD(month, INTERVAL 1 MONTH)
                    FROM months
                    WHERE month < DATE_FORMAT(:end_date, '%Y-%m-01')
                )

                SELECT
                    DATE_FORMAT(months.month, '%Y-%m') AS month,
                    COALESCE(SUM(copies.purchase_price), 0) AS spending
                FROM months
                LEFT JOIN copies
                    ON copies.purchase_date >= months.month
                    AND copies.purchase_date < DATE_ADD(months.month, INTERVAL 1 MONTH)
                    AND copies.purchase_date BETWEEN :start_date AND :end_date
                GROUP BY months.month
                ORDER BY months.month
            """),
            {
                "start_date": start_date,
                "end_date": end_date
            }
        ).mappings().all()

    return result

def get_overdue_loans():

    engine = create_engine(connection_str())

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    b.title,
                    CONCAT(f.f_name, ' ', f.l_name) AS friend,
                    l.loan_date,
                    l.due_date,
                    DATEDIFF(l.due_date, CURRENT_DATE()) AS days_remaining
                FROM loans l
                INNER JOIN copies c
                    ON l.copy_id = c.copy_id
                INNER JOIN books b
                    ON c.book_id = b.book_id
                INNER JOIN friends f
                    ON l.friend_id = f.friend_id
                WHERE l.return_date IS NULL
                ORDER BY l.due_date ASC
            """)
        ).mappings().all()

    return result

def get_top_books():
    engine = create_engine(connection_str())

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    b.title,
                    COUNT(l.loan_id) AS loan_count
                FROM loans l
                INNER JOIN copies c
                    ON l.copy_id = c.copy_id
                INNER JOIN books b
                    ON c.book_id = b.book_id
                GROUP BY b.book_id, b.title
                ORDER BY loan_count DESC
                LIMIT 5
            """)
        ).mappings().all()

    return result

def get_top_friends():
    engine = create_engine(connection_str())

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    CONCAT(f.f_name, ' ', f.l_name) AS friend,
                    COUNT(l.loan_id) AS loan_count
                FROM loans l
                INNER JOIN friends f
                    ON l.friend_id = f.friend_id
                GROUP BY f.friend_id, f.f_name, f.l_name
                ORDER BY loan_count DESC
                LIMIT 5
            """)
        ).mappings().all()

    return result

def get_top_authors():
    engine = create_engine(connection_str())

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    b.author,
                    COUNT(l.loan_id) AS loan_count
                FROM loans l
                INNER JOIN copies c
                    ON l.copy_id = c.copy_id
                INNER JOIN books b
                    ON c.book_id = b.book_id
                WHERE b.author IS NOT NULL
                  AND b.author <> ''
                GROUP BY b.author
                ORDER BY loan_count DESC
                LIMIT 5
            """)
        ).mappings().all()

    return result


print(get_top_authors())




