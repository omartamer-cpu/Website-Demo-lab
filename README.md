# Database Lab 2 — My Tasks

A website where users can create an account, log in, and manage their own tasks.

## Team

| Name | Student ID | Work |
|---|---|---|
| Omar Tamer Helmy | 2304084 | App , Gitignore , requiremnts , front end (Static) , Readme , Templates |
| Mohammed Elsayed | 2304061 | Schema , Test and Validation , Enviroment |

## Tools used

- Python and Flask
- MySQL and PyMySQL
- HTML, CSS, and JavaScript
- bcrypt for password hashing
- Flask-Session for server-side sessions

## Features

- Register an account and log in automatically (R1).
- Log in and log out (R2).
- Each user sees only their own tasks, with newest tasks first (R3).
- Add, edit, mark tasks done or open, and delete with confirmation (R4–R7).
- Check form inputs in the browser and on the server (R8).
- Use password hashes, parameterized SQL, and ownership checks (R9).
- Support desktop and mobile screens, with feedback and an empty list message (R10).
- Bonus features: dark mode with a saved preference, and All / Open / Done task filters.


## How to run on Windows

Install Python, Git, MySQL Server, and MySQL Workbench first. Make sure MySQL Server is running.


### 1. Download the project

The project files are on the Back-end branch:

```powershell
git clone --branch Back-end https://github.com/omartamer-cpu/Website-Demo-lab.git
cd Website-Demo-lab
```

### 2. Install the packages

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Set up the database

Open `database/schema.sql` in MySQL Workbench and run it.

Only do this for a new setup. Running it again deletes the existing database, including accounts and tasks.

### 4. Add your settings

```powershell
Copy-Item .env.example .env
```

Open `.env` and enter your MySQL username and password.

Generate a secret key:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Paste the result into `SECRET_KEY` in `.env`.

Keep `.env` private. It is excluded from Git.

### 5. Start the website

```powershell
.\.venv\Scripts\python.exe app.py
```

Open http://127.0.0.1:5000 in your browser.

Keep the terminal open while using the website. Press Ctrl+C to stop it.

## Screenshots

### Registration errors
![Registration errors](https://github.com/omartamer-cpu/Website-Demo-lab/blob/Back-end/Screenshots/register-errors.png?raw=true)

### Login page
![Login page](https://github.com/omartamer-cpu/Website-Demo-lab/blob/Back-end/Screenshots/login.png?raw=true)

### Task list
![Task list](https://github.com/omartamer-cpu/Website-Demo-lab/blob/Back-end/Screenshots/tasks.png?raw=true)

### Mobile view
![Mobile view](https://github.com/omartamer-cpu/Website-Demo-lab/blob/Back-end/Screenshots/Mobile.png?raw=true)

## Lab questions

(a)- Without AND user_id, a user could edit or delete another user's task by submitting its ID.
(b)- This is the referential integrity constraint.

### Why include user_id in UPDATE and DELETE?

It makes sure users can only change or delete their own tasks. The user ID comes from the login session.

### What happens if a task refers to a user who does not exist?

MySQL rejects it because of the foreign key. Every task must belong to an existing user.

### Why store a password hash?

The website can check passwords without saving the original password. bcrypt makes the hashes harder to crack.

### Why validate an empty name if the column uses NOT NULL?

NOT NULL prevents a NULL value, but it still allows an empty string. The website also checks for empty names and spaces.

## Testing

The following checks passed during manual testing:

- Registration errors and duplicate emails.
- Login, wrong passwords, and logout.
- Redirecting logged-out users away from the task page.
- Adding, editing, completing, and deleting tasks.
- Cancelling a deletion.
- Rejecting empty and spaces-only task titles.
- Keeping each account's tasks separate.
- Keeping saved changes after refreshing.
- SQL injection input and stored password hashes.
- Final mobile layout and screenshot links.
- Validation with JavaScript disabled.
- Titles longer than 200 characters.

Remaining checks before submission:

- Attempts to edit or delete another user's task directly.

## Main files

| File | Purpose |
|---|---|
| app.py | Backend, database queries, login, and task actions |
| database/schema.sql | Database tables and keys |
| templates/ | Website pages |
| static/style.css | Page design |
| static/validation.js | Form checks and delete confirmation |
| .env.example | Example settings |

## Repository

https://github.com/omartamer-cpu/Website-Demo-lab/tree/Back-end

The project is on the Back-end branch. If the repository is private, give the instructor access before submission.
