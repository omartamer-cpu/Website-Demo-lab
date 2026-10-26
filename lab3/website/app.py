"""Database Lab 2: plain SQL, server-side sessions, and personal tasks."""
import os
import secrets
import hashlib
import unicodedata
import warnings
from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge
from functools import wraps
from pathlib import Path
import bcrypt
import pymysql
from cachelib import FileSystemCache
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_session import Session
from decimal import Decimal, InvalidOperation

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


def get_db(database=None):
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '3306')),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=database or os.getenv('DB_NAME', 'registration'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def query(sql, values=(), write=False, database=None):
    connection = get_db(database)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)
            result = cursor.lastrowid if write else cursor.fetchall()
        if write:
            connection.commit()
        return result
    finally:
        connection.close()

def library_query(sql, values=(), write=False):
    return query(
        sql, values,
        write=write,
        database='lab3_library'
    )


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


# Library validation and optional image uploads.
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024
UPLOADS = BASE / 'static' / 'uploads'
UPLOADS.mkdir(parents=True, exist_ok=True)

def clean_text(value):
    return ' '.join(unicodedata.normalize('NFC', value).split())

def duplicate_key(*values):
    import json
    normalized = [clean_text(str(v)).casefold() for v in values]
    return hashlib.sha256(json.dumps(normalized, ensure_ascii=False).encode()).digest()

def letters_only(value):
    return bool(value) and any(c.isalpha() for c in value) and all(
        c.isalpha() or c == ' ' for c in value)

def save_image(upload):
    if not upload or not upload.filename:
        return None
    raw = upload.read(5 * 1024 * 1024 + 1)
    if len(raw) > 5 * 1024 * 1024:
        raise ValueError('Each image must be 5 MB or smaller.')
    from io import BytesIO
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(BytesIO(raw)) as im:
                if im.format not in ('JPEG', 'PNG', 'WEBP'):
                    raise ValueError('Choose a JPG, PNG, or WebP image.')
                if im.width * im.height > 20_000_000:
                    raise ValueError('Image is too large; use at most 20 megapixels.')
                im.load()
                im.thumbnail((1200, 1200))
                output = im.convert('RGB')
                filename = secrets.token_hex(16) + '.jpg'
                output.save(UPLOADS / filename, 'JPEG', quality=85)
                return filename
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError,
            Image.DecompressionBombWarning):
        raise ValueError('Upload a valid JPG, PNG, or WebP image.')

def remove_image(filename):
    # Only delete generated filenames, never a user-supplied path.
    if filename and len(filename) == 36 and filename.endswith('.jpg'):
        stem = filename[:-4]
        if all(c in '0123456789abcdef' for c in stem):
            (UPLOADS / filename).unlink(missing_ok=True)

@app.errorhandler(RequestEntityTooLarge)
def upload_too_large(error):
    return 'Upload too large. Choose an image under 5 MB, then go back.', 413

@app.get('/library')
@login_required
def library():
    authors = library_query('SELECT author_id, name, country, photo FROM AUTHOR ORDER BY author_id')
    books = library_query('SELECT book_id, title, price, author_id, cover FROM BOOK ORDER BY book_id')
    return render_template('library.html', authors=authors, books=books)

def author_values():
    name = clean_text(request.form.get('name', ''))
    country = clean_text(request.form.get('country', ''))
    if not letters_only(name) or len(name) > 100:
        raise ValueError('Author name must contain letters and spaces only (up to 100 characters).')
    if country and (not letters_only(country) or len(country) > 100):
        raise ValueError('Country must contain letters and spaces only (up to 100 characters).')
    return name, country

def book_values():
    title = clean_text(request.form.get('title', ''))
    try:
        price = Decimal(request.form.get('price', ''))
        author_id = int(request.form.get('author_id', ''))
        if (not title or len(title) > 200 or not price.is_finite()
            or price < 0 or price > Decimal('99999999.99')
            or price != price.quantize(Decimal('0.01')) or author_id <= 0):
            raise ValueError
    except (InvalidOperation, ValueError):
        raise ValueError('Enter a title, a valid price with at most two decimal places, and an author.')
    return title, price, author_id

def save_library_record(kind, record_id=None):
    author = kind == 'author'
    table, pk, image_col = ('AUTHOR', 'author_id', 'photo') if author else ('BOOK', 'book_id', 'cover')
    old = None
    if record_id is not None:
        rows = library_query(f'SELECT {image_col} FROM {table} WHERE {pk} = %s', (record_id,))
        if not rows:
            abort(404)
        old = rows[0][image_col]
    new = None
    try:
        values = author_values() if author else book_values()
        key = duplicate_key(*values) if author else duplicate_key(values[0], values[2])
        duplicates = library_query(f'SELECT {pk} FROM {table} WHERE duplicate_key = %s', (key,))
        if any(row[pk] != record_id for row in duplicates):
            raise ValueError('This author name and country already exist.' if author
                             else 'This title already exists for the selected author.')
        new = save_image(request.files.get(image_col))
        image_name = new or old
        if author:
            fields = 'name = %s, country = %s, duplicate_key = %s, photo = %s'
            insert_fields = 'name, country, duplicate_key, photo'
            params = (*values, key, image_name)
        else:
            fields = 'title = %s, price = %s, author_id = %s, duplicate_key = %s, cover = %s'
            insert_fields = 'title, price, author_id, duplicate_key, cover'
            params = (*values, key, image_name)
        if record_id is None:
            placeholders = ', '.join(['%s'] * len(params))
            library_query(f'INSERT INTO {table} ({insert_fields}) VALUES ({placeholders})', params, write=True)
        else:
            library_query(f'UPDATE {table} SET {fields} WHERE {pk} = %s', (*params, record_id), write=True)
    except ValueError as exc:
        remove_image(new)
        flash(str(exc))
    except pymysql.err.IntegrityError as exc:
        remove_image(new)
        if exc.args[0] == 1062:
            flash('That author name and country already exist.' if author else 'That book title and author already exist.')
        elif exc.args[0] == 1452:
            flash('The selected author no longer exists.')
        else:
            raise
    except Exception:
        remove_image(new)
        raise
    else:
        if new:
            remove_image(old)
        flash(kind.capitalize() + (' added.' if record_id is None else ' updated.'))
    return redirect(url_for('library'))

@app.post('/authors/add')
@login_required
def add_author():
    return save_library_record('author')

@app.post('/authors/<int:author_id>/edit')
@login_required
def edit_author(author_id):
    return save_library_record('author', author_id)

@app.post('/books/add')
@login_required
def add_book():
    return save_library_record('book')

@app.post('/books/<int:book_id>/edit')
@login_required
def edit_book(book_id):
    return save_library_record('book', book_id)

@app.post('/authors/<int:author_id>/delete')
@login_required
def delete_author(author_id):
    authors = library_query('SELECT photo FROM AUTHOR WHERE author_id = %s', (author_id,))
    if not authors:
        abort(404)
    books = library_query('SELECT cover FROM BOOK WHERE author_id = %s', (author_id,))
    library_query('DELETE FROM AUTHOR WHERE author_id = %s', (author_id,), write=True)
    remove_image(authors[0]['photo'])
    for book in books:
        remove_image(book['cover'])
    flash('Author and their books deleted.')
    return redirect(url_for('library'))

@app.post('/books/<int:book_id>/delete')
@login_required
def delete_book(book_id):
    books = library_query('SELECT cover FROM BOOK WHERE book_id = %s', (book_id,))
    if not books:
        abort(404)
    library_query('DELETE FROM BOOK WHERE book_id = %s', (book_id,), write=True)
    remove_image(books[0]['cover'])
    flash('Book deleted.')
    return redirect(url_for('library'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)
