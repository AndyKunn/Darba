# models.py

import sqlite3

def create_db():
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director TEXT,
            year INTEGER,
            genre TEXT
        )
    ''')

    conn.commit()
    conn.close()

create_db()
