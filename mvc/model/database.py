import sqlite3
import os

# path to the VOLog database file
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'volog.db')

# create and return db connection
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()

    # create the entry_log table if it does not exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS entry_log (
            entry_ID    INTEGER PRIMARY KEY AUTOINCREMENT,
            number_plate TEXT,
            headcount   INTEGER,
            timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
            gate_id     INTEGER
        )
    ''')

    # save
    conn.commit()
    conn.close()

def insert_entry(number_plate, headcount, gate_id):
    conn = get_connection()

    # creates cursor internally and disregards it straight away after use
    # insert new entry record into db
    conn.execute(
        'INSERT INTO entry_log (number_plate, headcount, gate_id) VALUES (?, ?, ?)',
        (number_plate, headcount, gate_id)
    )

    # save and close
    conn.commit()
    conn.close()


def get_all_entries():
    conn = get_connection()

    # retrieve all entries, most recent first
    rows = conn.execute(
        'SELECT * FROM entry_log ORDER BY timestamp DESC'
    ).fetchall()

    conn.close()

    # convert each row to a dictionary for easy JSON serialisation
    return [dict(row) for row in rows]