import sqlite3

DB_NAME = "holdings.db"

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
        shares INTEGER         
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dividends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        holding_id INTEGER NOT NULL,
        ex_dividend_date TEXT NOT NULL,
        record_date TEXT NOT NULL,
        payment_date TEXT NOT NULL,
        dividend_amount REAL NOT NULL,
        franking_percent REAL,
        FOREIGN KEY (holding_id) REFERENCES holdings (id)
    )
    """)

    conn.commit()
    conn.close()
