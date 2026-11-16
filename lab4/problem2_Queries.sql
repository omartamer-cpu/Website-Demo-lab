USE library;

-- F2.1  (sample values: keyword '1', price 10..30, category 1; the website passes them as placeholders)
SELECT b.book_id, b.title, b.price, c.name AS category
FROM book b JOIN category c ON b.category_id = c.category_id
WHERE b.title LIKE '%1%' AND b.price BETWEEN 10 AND 30 AND b.category_id = 1
ORDER BY b.price ASC;

-- F2.2
SELECT b.book_id, b.title, a.name AS author, p.name AS publisher, c.name AS category, b.price
FROM book b
JOIN author a    ON b.author_id = a.author_id
JOIN publisher p ON b.publisher_id = p.publisher_id
JOIN category c  ON b.category_id = c.category_id
ORDER BY b.book_id;

-- F2.3 (a)
SELECT c.name AS category, COUNT(*) AS books, AVG(b.price) AS avg_price
FROM category c JOIN book b ON b.category_id = c.category_id
GROUP BY c.category_id, c.name;

-- F2.3 (b)
SELECT a.name AS author, COUNT(*) AS books
FROM author a JOIN book b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name
HAVING COUNT(*) >= 2;

-- F2.3 (c)
SELECT SUM(price) AS total_price, MIN(price) AS smallest_price, MAX(price) AS largest_price
FROM book;

-- F2.4 (a)
SELECT l.loan_id, b.title, m.name AS member, l.loan_date
FROM loan l JOIN book b ON l.book_id = b.book_id JOIN member m ON l.member_id = m.member_id
WHERE l.return_date IS NULL;

-- F2.4 (b)
SELECT m.member_id, m.name
FROM member m LEFT JOIN loan l ON l.member_id = m.member_id
WHERE l.loan_id IS NULL;

-- F2.4 (c)
SELECT b.book_id, b.title
FROM book b LEFT JOIN loan l ON l.book_id = b.book_id
WHERE l.loan_id IS NULL;

-- F2.5 (3 most borrowed books; ties broken by title)
SELECT b.title, COUNT(*) AS loans
FROM book b JOIN loan l ON l.book_id = b.book_id
GROUP BY b.book_id, b.title
ORDER BY loans DESC, b.title
LIMIT 3;

-- F2.5 (member with the most loans)
SELECT m.name, COUNT(*) AS loans
FROM member m JOIN loan l ON l.member_id = m.member_id
GROUP BY m.member_id, m.name
ORDER BY loans DESC, m.name
LIMIT 1;

-- F2.6 (a)
SELECT a.name AS author, COUNT(b.book_id) AS books
FROM author a LEFT JOIN book b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name;

-- F2.6 (b)
SELECT b.title, a.name AS author, p.name AS publisher, a.country
FROM book b
JOIN author a    ON b.author_id = a.author_id
JOIN publisher p ON b.publisher_id = p.publisher_id
WHERE a.country = p.country;
