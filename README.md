# My Tasks — Database Lab 2

## Team
- Name: **FILL IN YOUR NAME**
- Student ID: **FILL IN YOUR ID**
- Contributions: **Describe what you implemented and reviewed.**
- If working with a partner, add their name, ID, and contributions. Both members must have commits.

## Technologies
Python / Flask backend; HTML, CSS, JavaScript and Jinja templates; MySQL database; PyMySQL with plain parameterized SQL; bcrypt password hashing; Flask-Session with a local server-side cache.

## Windows setup (PowerShell)
1. Install Python, MySQL Server, MySQL Workbench, and Git. MySQL Server must be running.
2. Extract this project and open its folder in VS Code. Open Terminal → New Terminal.
3. Create the environment and install dependencies:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
   No environment activation is needed.
4. In MySQL Workbench, connect to your server. Open `database/schema.sql` and run the whole script. **This deletes existing data in registration. If you already created the same tables, skip this step.**
5. Copy the example configuration:
   ```powershell
   Copy-Item .env.example .env
   ```
6. Edit `.env`: enter your MySQL password and username. Do not share or commit this file. Generate a session secret:
   ```powershell
   .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the printed value into `SECRET_KEY` in `.env`.
7. Check the database:
   ```powershell
   .\.venv\Scripts\python.exe test_db.py
   ```
   Expected: `Connected successfully!`, `todos`, `users`.
8. Start the server:
   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```
9. Open http://127.0.0.1:5000 in your browser. Keep the terminal open. Ctrl+C stops the server.

If you already have `.venv`, reuse it. Keep your existing `.env` credentials, but add `SECRET_KEY`. If port 5000 is occupied, stop the other server or change the port in `app.py`.

## Features (R1–R10)
- R1: registration; duplicate email feedback; automatic login after registration.
- R2: login with a single invalid-credentials message; logout.
- R3: private lists, newest first, separate for each user.
- R4–R7: add, edit, mark done/open, delete after confirmation.
- R8: browser and server validation, exact required messages.
- R9: bcrypt hashes, SQL parameters, user ID from the session.
- R10: consistent responsive design, empty state, feedback, user name and logout.
- Additional protection: CSRF tokens and session regeneration at login.
- No bonus is claimed.

## Required screenshots — add these before submission
Store real screenshots from your running application in `screenshots/` with these filenames. Images appear below once you add them.

### Register with errors
![Register errors](screenshots/register-errors.png)

### Login
![Login](screenshots/login.png)

### List with tasks, including one completed
![Tasks](screenshots/tasks.png)

### Phone-sized view (360 pixels wide)
![Mobile](screenshots/mobile.png)

Use Chrome/Edge F12, then Ctrl+Shift+M and set width 360. Capture the site, not passwords or `.env`.

## Questions
**(a) Why AND user_id in UPDATE/DELETE?**
It restricts the change to a task owned by the logged-in user. Without it, a user could submit another person's task ID and edit/delete their task. The owner ID must come from the session, not the browser.

**(b) What if a task references a missing user?**
MySQL rejects the INSERT because the foreign key requires a matching users.user_id. This is referential integrity.

**(c) Why a hash instead of the password?**
A password hash allows password verification without storing the original password. bcrypt adds a salt and intentionally expensive processing, making stolen hashes harder to crack. Hashing is not reversible encryption.

**(d) Why check an empty name when NOT NULL is present?**
NOT NULL rejects NULL, but accepts an empty string. The application must reject empty names and names containing only spaces.

## Manual checks before submission
- Open /todos while logged out: redirected to login.
- Submit empty registration: every required-field message appears; repeat with JavaScript disabled to check the server.
- Register a duplicate email: Email Already Exists.
- Unknown email and wrong password: Invalid email or password.
- Try `' OR '1'='1' --` as email: no login.
- Register two users using normal and incognito windows. Their tasks must remain separate.
- In browser developer tools, change an edit/delete form action to another user's task ID, keeping the current user's CSRF token: the other user's task must not change.
- Empty/spaces-only title and 201-character title: rejected; no database change.
- Add, edit, toggle, cancel delete, confirm delete; logout and revisit /todos.
- Inspect `SELECT password_hash FROM registration.users;`: only hashes, never original passwords.
- Check at 360px width and on laptop.
- Restart the app and confirm data remains in MySQL.

## GitHub submission
Create a GitHub repository without initializing a README, then run from this project folder:
```powershell
git init
git add .
git commit -m "Add login and personal tasks application"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```
Replace the URL. Commit incrementally as you review and customize; do not invent contribution history. If private, share with the TA usernames they provide. Check `.env` is not tracked (`git ls-files .env` should print nothing). Submit the repository URL through the course submission method.

## Reading the code
- `app.py`: routes, validation, hashing, database access, and sessions.
- `templates/auth.html`: reusable register/login page.
- `templates/todos.html`: task forms and list.
- `static/validation.js`: browser validation and delete confirmation.
- `static/style.css`: appearance and phone layout.
- `database/schema.sql`: creates the two tables and their constraints.

GET shows a page. POST processes a form. Successful POSTs redirect, avoiding duplicate submissions on refresh. PyMySQL uses `%s` rather than the handout's `?` placeholders, passing values separately. `query(..., write=True)` commits a database change; SELECT returns rows. Learn each route and customize this project so you can explain it to your TA.

Delete confirmation uses browser JavaScript; keep JavaScript enabled for the normal application. With JavaScript disabled, server validation still works, but the confirmation dialog does not appear.

## Verification status
See `VERIFICATION.txt` for checks actually performed in the preparation environment. MySQL integration, browser screenshots, and final setup on your Windows machine still need verification.
