CREATE SCHEMA IF NOT EXISTS lianes_library;
USE lianes_library;

-- =========================
-- SCHEMA
-- =========================

CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    genre VARCHAR(100),
    isbn VARCHAR(20),
    publicationyear SMALLINT
);

CREATE TABLE copies (
    copy_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    copy_status VARCHAR(50) NOT NULL,
    purchase_price DECIMAL(10,2) DEFAULT 0.0,
    purchase_date DATE NOT NULL DEFAULT(CURRENT_DATE()),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE friends (
    friend_id INT AUTO_INCREMENT PRIMARY KEY,
    f_name VARCHAR(255) NOT NULL,
    l_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(30),
    adress VARCHAR(255),
    max_loans TINYINT DEFAULT 3,
    is_trusted BOOLEAN NOT NULL DEFAULT TRUE,
    friend_notes TEXT
);

CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    copy_id INT NOT NULL,
    friend_id INT NOT NULL,
    loan_date DATE DEFAULT(CURRENT_DATE()) NOT NULL,
    due_date DATE DEFAULT(DATE_ADD(loan_date, INTERVAL 30 DAY)),
    return_date DATE,
    FOREIGN KEY (copy_id) REFERENCES copies(copy_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (friend_id) REFERENCES friends(friend_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- =========================
-- DEMO DATA
-- =========================

-- 1000 books
INSERT INTO books (title, author, genre, isbn, publicationyear)
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL SELECT n + 1 FROM numbers WHERE n < 1000
)
SELECT
    CONCAT('Book ', n),
    CONCAT('Author ', ((n - 1) % 300) + 1),
    CASE
        WHEN n % 10 = 0 THEN 'Crime'
        WHEN n % 10 = 1 THEN 'History'
        WHEN n % 10 = 2 THEN 'Political'
        WHEN n % 10 = 3 THEN 'Literature'
        WHEN n % 10 = 4 THEN 'Adventure'
        WHEN n % 10 = 5 THEN 'Science'
        WHEN n % 10 = 6 THEN 'Fantasy'
        WHEN n % 10 = 7 THEN 'Biography'
        WHEN n % 10 = 8 THEN 'Romance'
        ELSE 'Drama'
    END,
    CONCAT('978-', LPAD(n, 10, '0')),
    1950 + (n % 76)
FROM numbers;

-- 1300 copies:
-- books 1-700: one copy
-- books 701-1000: two copies
INSERT INTO copies (book_id, copy_status, purchase_price, purchase_date)
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL SELECT n + 1 FROM numbers WHERE n < 1000
),
copies_to_create AS (
    SELECT n AS book_id, 1 AS copy_number FROM numbers
    UNION ALL
    SELECT n AS book_id, 2 AS copy_number FROM numbers WHERE n > 700
)
SELECT
    book_id,
    CASE
        WHEN book_id <= 25 AND copy_number = 1 THEN 'Borrowed'
        WHEN book_id BETWEEN 26 AND 50 AND copy_number = 1 THEN 'Lost'
        WHEN book_id BETWEEN 51 AND 75 AND copy_number = 1 THEN 'Worn out'
        ELSE 'Available'
    END,
    ROUND(8 + ((book_id * 7 + copy_number * 13) % 500) / 10, 2),
    DATE_ADD('2024-01-01',
        INTERVAL ((book_id * 17 + copy_number * 31) % 990) DAY)
FROM copies_to_create;

-- 100 friends
INSERT INTO friends
    (f_name, l_name, email, phone, adress, max_loans, is_trusted, friend_notes)
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL SELECT n + 1 FROM numbers WHERE n < 100
)
SELECT
    CONCAT('Friend', n),
    CONCAT('Lastname', n),
    CONCAT('friend', n, '@example.com'),
    CONCAT('+49170', LPAD(n, 6, '0')),
    CONCAT('Example Street ', n, ', Gelsenkirchen'),
    3,
    CASE WHEN n % 10 = 0 THEN FALSE ELSE TRUE END,
    CASE WHEN n % 10 = 0 THEN 'Lost a book previously' ELSE NULL END
FROM numbers;

-- 300 completed loans
-- All loan dates and return dates are within 2024-2026.
INSERT INTO loans (copy_id, friend_id, loan_date, due_date, return_date)
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL SELECT n + 1 FROM numbers WHERE n < 300
)
SELECT
    n,
    ((n - 1) % 100) + 1,
    DATE_ADD('2024-01-01', INTERVAL ((n * 7) % 980) DAY),
    DATE_ADD(DATE_ADD('2024-01-01', INTERVAL ((n * 7) % 980) DAY), INTERVAL 30 DAY),
    DATE_ADD(DATE_ADD('2024-01-01', INTERVAL ((n * 7) % 980) DAY), INTERVAL (10 + (n % 20)) DAY)
FROM numbers;

-- 50 open loans
-- 10 overdue loans + 40 non-overdue loans.
-- All loan dates are within 2024-2026.
INSERT INTO loans (copy_id, friend_id, loan_date, due_date, return_date)
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL SELECT n + 1 FROM numbers WHERE n < 50
)
SELECT
    300 + n,
    ((n - 1) % 100) + 1,
    CASE
        WHEN n <= 10 THEN DATE_SUB(CURRENT_DATE(), INTERVAL (45 - n) DAY)
        ELSE DATE_SUB(CURRENT_DATE(), INTERVAL (20 + (n % 10)) DAY)
    END,
    CASE
        WHEN n <= 10 THEN DATE_SUB(CURRENT_DATE(), INTERVAL (15 - n) DAY)
        ELSE DATE_ADD(CURRENT_DATE(), INTERVAL (n - 10) DAY)
    END,
    NULL
FROM numbers;

-- =========================
-- CHECKS
-- =========================

SELECT COUNT(*) AS number_of_books FROM books;
SELECT COUNT(*) AS number_of_copies FROM copies;
SELECT COUNT(*) AS number_of_friends FROM friends;
SELECT COUNT(*) AS number_of_loans FROM loans;

SELECT copy_status, COUNT(*) AS number_of_copies
FROM copies
GROUP BY copy_status;

SELECT COUNT(*) AS open_loans
FROM loans
WHERE return_date IS NULL;

SELECT COUNT(*) AS overdue_open_loans
FROM loans
WHERE return_date IS NULL
  AND due_date < CURRENT_DATE();

SELECT COUNT(*) AS non_overdue_open_loans
FROM loans
WHERE return_date IS NULL
  AND due_date >= CURRENT_DATE();

SELECT MIN(purchase_date) AS first_purchase_date,
       MAX(purchase_date) AS last_purchase_date
FROM copies;

SELECT MIN(loan_date) AS first_loan_date,
       MAX(loan_date) AS last_loan_date
FROM loans;

SELECT COUNT(*) AS inconsistent_open_loans
FROM loans l
JOIN copies c ON l.copy_id = c.copy_id
WHERE l.return_date IS NULL
  AND c.copy_status <> 'Borrowed';
