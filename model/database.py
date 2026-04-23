import sqlite3
import os

# specifying the name of the volog database
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'volog.db')

# getting a connection and 
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS entry_log (
            entry_ID    INTEGER PRIMARY KEY AUTOINCREMENT,
            number_plate TEXT,
            headcount   INTEGER,
            timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
            gate_id     INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_entry(number_plate, headcount, gate_id):
    conn = get_connection()
    # creates cursor internally and disregards it straight away after use
    conn.execute(
        'INSERT INTO entry_log (number_plate, headcount, gate_id) VALUES (?, ?, ?)',
        (number_plate, headcount, gate_id)
    )
    conn.commit()
    conn.close()

def get_all_entries():
    conn = get_connection()
    rows = conn.execute(
        'SELECT * FROM entry_log ORDER BY timestamp DESC'
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]