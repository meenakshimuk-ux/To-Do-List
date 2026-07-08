import os
import sqlite3
from app import app, db
from models import Task

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'todo.db')

NEW_COLUMNS = [
    ('category', "VARCHAR(20) DEFAULT 'general'"),
    ('notes', 'TEXT'),
    ('updated_at', 'DATETIME'),
]


def migrate_schema():
    """Add new columns to existing database if needed."""
    if not os.path.exists(DB_PATH):
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(task)")
    existing = {row[1] for row in cursor.fetchall()}

    for col_name, col_type in NEW_COLUMNS:
        if col_name not in existing:
            cursor.execute(f'ALTER TABLE task ADD COLUMN {col_name} {col_type}')
            print(f'Added column: {col_name}')

    conn.commit()
    conn.close()


with app.app_context():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db.create_all()
    migrate_schema()
    print('Database initialized successfully!')
