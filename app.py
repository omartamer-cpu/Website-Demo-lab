"""Database Lab 2: plain SQL, server-side sessions, and personal tasks."""
import os
import secrets
from functools import wraps
from pathlib import Path
import bcrypt
import pymysql
from cachelib import FileSystemCache
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_session import Session

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / '.env')
app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ['SECRET_KEY'],
    SESSION_TYPE='cachelib',
    SESSION_CACHELIB=FileSystemCache(str(BASE / 'instance' / 'sessions'), threshold=500),
    SESSION_PERMANENT=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
Session(app)


def get_db():
    return pymysql.connect(host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '3306')), user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''), database=os.getenv('DB_NAME', 'registration'),
        charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def query(sql, values=(), write=False):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)
            result = cursor.lastrowid if write else cursor.fetchall()
        if write:
            connection.commit()
        return result
    finally:
        connection.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

app.jinja_env.globals['csrf_token'] = csrf_token

@app.before_request
def protect_forms():
    if request.method == 'POST':
        expected = session.get('csrf_token', '')
        supplied = request.form.get('csrf_token', '')
        if not expected or not secrets.compare_digest(expected, supplied):
            abort(400)


def establish_session(user_id, name):
    session.clear()
    session['user_id'] = user_id
    session['name'] = name
    app.session_interface.regenerate(session)

@app.route('/')
def home():
    return redirect(url_for('todos' if 'user_id' in session else 'login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = {}
    name = email = ''
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        for key, value, message in [('name', name, 'Name is required'),
            ('email', email, 'Email is required'), ('password', password, 'Password is required'),
            ('confirm_password', confirm, 'Confirm password is required')]:
            if not value:
                errors[key] = message
        if password and confirm and password != confirm:
            errors['confirm_password'] = 'Passwords do not match'
        if len(name) > 100:
            errors['name'] = 'Name is too long (100 characters at most)'
        if len(email) > 255:
            errors['email'] = 'Email is too long (255 characters at most)'
        if len(password.encode('utf-8')) > 72:
            errors['password'] = 'Password is too long (72 UTF-8 bytes at most)'
        if not errors:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            try:
                user_id = query('INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)',
                    (email, name, hashed), write=True)
            except pymysql.err.IntegrityError as exc:
                if exc.args[0] != 1062:
                    raise
                errors['email'] = 'Email Already Exists'
            else:
                establish_session(user_id, name)
                return redirect(url_for('todos'))
    return render_template('auth.html', registering=True, errors=errors, name=name, email=email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}
    email = ''
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        if not email:
            errors['email'] = 'Email is required'
        if not password:
            errors['password'] = 'Password is required'
        if not errors:
            users = query('SELECT user_id, name, password_hash FROM users WHERE email = %s', (email,))
            valid = False
            if users:
                try:
                    valid = bcrypt.checkpw(password.encode('utf-8'), users[0]['password_hash'].encode('utf-8'))
                except ValueError:
                    valid = False
            if valid:
                establish_session(users[0]['user_id'], users[0]['name'])
                return redirect(url_for('todos'))
            errors['general'] = 'Invalid email or password'
    return render_template('auth.html', registering=False, errors=errors, email=email)

@app.post('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


def render_list(errors=None, add_title='', edit_id=None, edit_title=''):
    rows = query('SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC',
        (session['user_id'],))
    return render_template('todos.html', rows=rows, errors=errors or {}, add_title=add_title,
        edit_id=edit_id, edit_title=edit_title)


def title_errors(title):
    if not title:
        return {'title': 'Title is required'}
    if len(title) > 200:
        return {'title': 'Title is too long'}
    return {}

@app.get('/todos')
@login_required
def todos():
    return render_list()

@app.post('/todos/add')
@login_required
def add_todo():
    title = request.form.get('title', '').strip()
    errors = title_errors(title)
    if errors:
        return render_list(errors, add_title=title)
    query('INSERT INTO todos (user_id, title) VALUES (%s, %s)', (session['user_id'], title), write=True)
    flash('Task added.')
    return redirect(url_for('todos'))

@app.post('/todos/<int:todo_id>/edit')
@login_required
def edit_todo(todo_id):
    title = request.form.get('title', '').strip()
    errors = title_errors(title)
    if errors:
        return render_list(errors, edit_id=todo_id, edit_title=title)
    query('UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s',
        (title, todo_id, session['user_id']), write=True)
    return redirect(url_for('todos'))

@app.post('/todos/<int:todo_id>/toggle')
@login_required
def toggle_todo(todo_id):
    is_done = request.form.get('is_done')
    if is_done not in ('0', '1'):
        abort(400)
    query('UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s',
        (int(is_done), todo_id, session['user_id']), write=True)
    return redirect(url_for('todos'))

@app.post('/todos/<int:todo_id>/delete')
@login_required
def delete_todo(todo_id):
    query('DELETE FROM todos WHERE todo_id = %s AND user_id = %s',
        (todo_id, session['user_id']), write=True)
    flash('Task deleted.')
    return redirect(url_for('todos'))

@app.errorhandler(pymysql.MySQLError)
def database_error(error):
    app.logger.error('Database request failed: %s', type(error).__name__)
    return render_template('error.html', message='Database connection failed. Check your .env settings and that MySQL is running.'), 503

@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html', message='This form could not be submitted. Reload the page and try again.'), 400

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message='That page could not be found.'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', message='Something went wrong. Please try again.'), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
