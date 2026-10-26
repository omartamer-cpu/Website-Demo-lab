# Database Lab 3

**Name:** Omar Tamer Helmy  
**Student ID:** 2304084

## Overview

This project demonstrates SQL tables, primary keys, foreign keys,
referential integrity, and a Flask website for managing authors and books.

## Project Files

- `problem1_DDL.sql`: Creates the company database and its tables.
- `problem1_DML.sql`: Inserts sample departments, employees, and projects.
- `problem1_Answers.txt`: Answers and results for the foreign key questions.
- `problem2_DDL.sql`: Creates the authors and books database.
- `problem2_DML.sql`: Inserts 3 authors and 6 books.
- `website/`: Flask application continued from Lab 2.

## Website Features

- Registration and login with bcrypt password hashing.
- Server-side sessions and CSRF protection.
- Personal task management from Lab 2.
- Display authors and books in separate tables.
- Add, edit, and delete authors.
- Add, edit, and delete books.
- Select a book's author using a dropdown.
- Automatically delete an author's books using ON DELETE CASCADE.
- Parameterized SQL queries and server-side input validation.

## Requirements

- Python
- MySQL Server
- MySQL Workbench

## Setup

### 1. Prepare the databases

Run these scripts in MySQL Workbench in this order:

1. `problem1_DDL.sql`
2. `problem1_DML.sql`
3. `problem2_DDL.sql`
4. `problem2_DML.sql`

The Problem 1 DDL script resets the `company` database.
Run the sample-data scripts once on newly created tables.

For a fresh installation, also run `website/database/schema.sql`
to prepare the Lab 2 login and tasks database.

### 2. Install Python packages

Open a terminal inside `website` and run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Configure the environment

Copy `.env.example` to `.env` and enter your local MySQL settings:

```dotenv
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=registration
SECRET_KEY=your_random_secret_key
```

Use the actual Lab 2 database name if it differs from `registration`.
The authors and books features connect separately to `lab3_library`.

Never commit `.env` to GitHub.

### 4. Run the website

From the `website` folder:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open http://127.0.0.1:5001, register or log in, then click **Library**.

## Manual Testing

- Displayed the seeded authors and books.
- Added an author and a book.
- Edited an author's details.
- Edited a book's title, price, and author.
- Deleted a book.
- Deleted a test author and confirmed their book was automatically deleted.
- Confirmed Problem 1 rejects deletion of a referenced employee.
- Confirmed Problem 1 rejects a project with a nonexistent department.

## Technologies

Python, Flask, MySQL, PyMySQL, HTML, CSS, JavaScript,
bcrypt, python-dotenv, and Flask-Session.