import sqlite3
from app.get_dividend_info import get_next_dividend  
from app.get_dividend_info import fetch_franking_percent     

def view_tables():
    # Connect to the database
    conn = sqlite3.connect('holdings.db')  # Replace with your actual database name
    cursor = conn.cursor()

    # Retrieve data from holdings table
    print("Holdings Table:")
    cursor.execute("SELECT * FROM holdings")
    holdings = cursor.fetchall()
    for row in holdings:
        print(row)

    holdings_ids = [row[0] for row in holdings]  # Extract holding IDs for dividends

    print(get_next_dividend(ticker = holdings_ids[1]))
    
    # Retrieve data from dividends table
    print("\nDividends Table:")
    cursor.execute("SELECT * FROM dividends")
    dividends = cursor.fetchall()
    for row in dividends:
        print(row)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    # view_tables()

    print(fetch_franking_percent(ticker = "CBA"))  # Example ticker, replace with actual ticker
    