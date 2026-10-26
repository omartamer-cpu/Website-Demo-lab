"""Run once after installing requirements, with Flask stopped. Does not delete rows."""
from app import get_db, clean_text, duplicate_key

def main():
    db = get_db('lab3_library')
    try:
        with db.cursor() as cur:
            plans = []
            for table, pk, fields, image in [
                ('AUTHOR', 'author_id', ('name', 'country'), 'photo'),
                ('BOOK', 'book_id', ('title', 'author_id'), 'cover')]:
                cur.execute(f'SELECT * FROM {table}')
                rows = cur.fetchall()
                seen = {}
                updates = []
                for row in rows:
                    vals = [row[f] if row[f] is not None else '' for f in fields]
                    key = duplicate_key(*vals)
                    if key in seen:
                        raise ValueError(f'{table}: duplicate IDs {seen[key]} and {row[pk]}. Edit or delete one through the OLD website, then rerun. No records were deleted.')
                    seen[key] = row[pk]
                    updates.append((key, row[pk]))
                plans.append((table, pk, image, updates))
            # All duplicate checks finish before schema changes begin.
            for table, pk, image, updates in plans:
                cur.execute(f'SHOW COLUMNS FROM {table}')
                columns = {c['Field'] for c in cur.fetchall()}
                if image not in columns:
                    cur.execute(f'ALTER TABLE {table} ADD COLUMN {image} VARCHAR(80) NULL')
                if 'duplicate_key' not in columns:
                    cur.execute(f'ALTER TABLE {table} ADD COLUMN duplicate_key BINARY(32) NULL')
                for key, row_id in updates:
                    cur.execute(f'UPDATE {table} SET duplicate_key = %s WHERE {pk} = %s', (key, row_id))
                db.commit()
                cur.execute(f'ALTER TABLE {table} MODIFY duplicate_key BINARY(32) NOT NULL')
                cur.execute(f'SHOW INDEX FROM {table}')
                if 'uq_duplicate' not in {i['Key_name'] for i in cur.fetchall()}:
                    cur.execute(f'ALTER TABLE {table} ADD UNIQUE KEY uq_duplicate (duplicate_key)')
        print('Upgrade complete. Records preserved. Start app.py now.')
    finally:
        db.close()

if __name__ == '__main__':
    main()
