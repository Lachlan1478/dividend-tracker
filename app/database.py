import sqlite3

DB_NAME = "dividends.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Holdings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS holdings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        shares INTEGER NOT NULL,
        ex_dividend_date TEXT,
        record_date TEXT,
        payment_date TEXT,
        dividend_amount REAL,
        franking_percent REAL           
    )
    """)

    conn.commit()
    conn.close()
