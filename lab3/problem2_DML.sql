USE lab3_library;

INSERT INTO AUTHOR (author_id, name, country) VALUES
(1, 'Naguib Mahfouz', 'Egypt'),
(2, 'George Orwell', 'United Kingdom'),
(3, 'Jane Austen', 'United Kingdom');

INSERT INTO BOOK (book_id, title, price, author_id) VALUES
(1, 'Palace Walk', 150.00, 1),
(2, 'Midaq Alley', 120.00, 1),
(3, '1984', 180.00, 2),
(4, 'Animal Farm', 100.00, 2),
(5, 'Pride and Prejudice', 160.00, 3),
(6, 'Emma', 140.00, 3);

SELECT * FROM AUTHOR;
SELECT * FROM BOOK;