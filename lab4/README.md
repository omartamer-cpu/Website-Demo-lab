# Lab 4 - Search Queries in SQL

Group members: <names and ids>

## Requirements
MySQL 8 (client + server), PHP 8 with the `pdo_mysql` extension.

## Problem 1 (database `company`)
```
mysql -u root -p < problem1_DDL.sql     # creates the database and 5 tables
mysql -u root -p < problem1_DML.sql     # inserts the rows
```
`problem1_Answers.txt` has the SQL and output/error of Q1.1-Q1.12. To replay them: `mysql -u root -p company`
and paste the statements in order (Q1.1-Q1.3 change the data).

## Problem 2 (database `library`)
```
mysql -u root -p < problem2_DDL.sql     # six tables, ON DELETE CASCADE
mysql -u root -p < problem2_DML.sql     # seed data
mysql -u root -p < problem2_Queries.sql # the SQL of F2.1-F2.6 (optional check)
```

## Website
1. Open `website/db.php` and set the MySQL user/password (or set `DB_USER` / `DB_PASS`).
2. Copy the `website/` pages next to your Lab 3 pages, or run on their own:
   ```
   cd website
   php -S localhost:8000
   ```
3. Open http://localhost:8000/ and use the menu: F2.1 Search, F2.2 Catalogue, F2.3 Reports,
   F2.4 Loans, F2.5 Most borrowed, F2.6 Authors and books.

F2.1 uses prepared statements (placeholders `?`) - bonus.
