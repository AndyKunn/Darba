# dataloader.py

import sqlite3

def add_film(title, director, year, genre):
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO films (title, director, year, genre)
        VALUES (?, ?, ?, ?)
    ''', (title, director, year, genre))

    conn.commit()
    conn.close()
