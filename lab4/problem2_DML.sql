USE library;

-- Authors 1 and 2 share a country; author 5 has no books; authors 1, 3, 4 wrote 2+ books
INSERT INTO author (author_id, name, country) VALUES
(1,'Naguib Mahfouz','Egypt'),(2,'Taha Hussein','Egypt'),
(3,'George Orwell','UK'),(4,'Carl Sagan','USA'),(5,'Haruki Murakami','Japan');

-- Egypt and UK publishers match an author's country; Hachette (France) matches none
INSERT INTO publisher (publisher_id, name, country) VALUES
(1,'Dar El Shorouk','Egypt'),(2,'Penguin','UK'),(3,'Hachette','France');

INSERT INTO category (category_id, name) VALUES (1,'Fiction'),(2,'History'),(3,'Science');

-- Book 1 costs between 15 and 20; books 3, 5, 10 are never borrowed
INSERT INTO book (book_id, title, price, publish_year, author_id, publisher_id, category_id) VALUES
(1,'Palace Walk',18.50,2019,1,1,1),
(2,'Sugar Street',22.00,2018,1,1,1),
(3,'Midaq Alley',14.00,2020,1,1,1),
(4,'The Days',12.50,2017,2,1,2),
(5,'On Pre-Islamic Poetry',25.00,2016,2,1,2),
(6,'1984',16.00,2021,3,2,1),
(7,'Animal Farm',11.00,2020,3,2,1),
(8,'Homage to Catalonia',19.00,2015,3,2,2),
(9,'Cosmos',28.00,2013,4,3,3),
(10,'Pale Blue Dot',21.00,2014,4,3,3);

-- Member 5 has no loans
INSERT INTO member (member_id, name, email, join_date) VALUES
(1,'Ali Samy','ali@mail.com','2026-01-10'),(2,'Mona Adel','mona@mail.com','2026-02-15'),
(3,'Karim Nader','karim@mail.com','2026-03-20'),(4,'Dina Farouk','dina@mail.com','2026-04-05'),
(5,'Hassan Gamal','hassan@mail.com','2026-05-01');

-- Loans 5, 7 are not returned yet
INSERT INTO loan (loan_id, book_id, member_id, loan_date, return_date) VALUES
(1,1,1,'2026-09-01','2026-09-10'),(2,1,2,'2026-09-12','2026-09-20'),
(3,1,3,'2026-10-01','2026-10-08'),(4,2,1,'2026-09-05','2026-09-15'),
(5,2,2,'2026-10-02',NULL),(6,6,1,'2026-10-05','2026-10-12'),
(7,6,3,'2026-10-15',NULL),(8,7,4,'2026-09-20','2026-09-27'),
(9,8,4,'2026-10-10','2026-10-18'),(10,4,2,'2026-10-20','2026-10-28'),
(11,9,3,'2026-10-22','2026-10-30'),(12,4,1,'2026-11-02','2026-11-09');
