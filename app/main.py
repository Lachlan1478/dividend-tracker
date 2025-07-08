from fastapi import FastAPI, HTTPException, Path
import yfinance as yf
import pandas as pd
from pydantic import BaseModel
from app.models import DividendCreate
from app.database import create_tables, get_connection
from app.get_dividend_info import get_next_dividend

# ================================================== #
#  1.0 Start up 
# ================================================== #
app = FastAPI()

# Run this on startup
@app.on_event("startup")
def on_startup():
    create_tables()

# Pydantic model for new holdings
class Holding(BaseModel):
    ticker: str
    shares: int

# Home route
@app.get("/")
def read_root():
    return {"message": "Dividend Tracker API is running"}


# ================================================== #
#  2.0) Holdings Endpoints
# ================================================== #

# GET all holdings
@app.get("/holdings")
def get_holdings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM holdings ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

     # Format for frontend
    holdings_keys = ["id", "ticker", "shares"]
    return [dict(zip(holdings_keys, row)) for row in rows]

# POST new holding
@app.post("/holdings")
def add_holding(holding: Holding):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO holdings (ticker, shares) VALUES (?, ?)",
            (holding.ticker.upper(), holding.shares)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    
    conn.close()
    return {"message": f"Added {holding.shares} shares of {holding.ticker.upper()}"}

@app.delete("/holdings/{holding_id}")
def delete_holding(holding_id: int = Path(..., description="ID of the holding to delete")):
    conn = get_connection()
    cursor = conn.cursor()

    # First delete related dividends
    cursor.execute("DELETE FROM dividends WHERE holding_id = ?", (holding_id,))
    # Then delete the holding
    cursor.execute("DELETE FROM holdings WHERE id = ?", (holding_id,))
    conn.commit()
    conn.close()

    return {"message": f"Holding {holding_id} and related dividends deleted"}

# ================================================== #
# 3.0) Dividends Endpoints
# ================================================== #

@app.get("/dividends")
def get_dividends():
    conn = get_connection()
    cursor = conn.cursor()

    # --- Sync logic ---
    cursor.execute("SELECT id FROM holdings")
    holding_ids = set(row[0] for row in cursor.fetchall())

    cursor.execute("SELECT DISTINCT holding_id FROM dividends")
    dividend_ids = set(row[0] for row in cursor.fetchall())

    # Add missing dividend rows
    for hid in holding_ids - dividend_ids:
        # Get the ticker for this holding_id
        cursor.execute("SELECT ticker FROM holdings WHERE id = ?", (hid,))
        result = cursor.fetchone()
        if result:
            ticker = result[0]
            dividend_data = get_next_dividend(ticker)

            if dividend_data:
                cursor.execute("""
                    INSERT INTO dividends (
                        holding_id, ex_dividend_date, record_date, payment_date,
                        dividend_amount, franking_percent
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    hid,
                    dividend_data.get("ex_dividend_date", ""),
                    dividend_data.get("record_date", ""),
                    dividend_data.get("payment_date", ""),
                    dividend_data.get("dividend_amount", 0.0),
                    dividend_data.get("franking_percent", 0.0)
                ))
            else:
                # Optional: fallback insert if no data is available
                cursor.execute("""
                    INSERT INTO dividends (
                        holding_id, ex_dividend_date, record_date, payment_date,
                        dividend_amount, franking_percent
                    ) VALUES (?, '', '', '', 0.0, 0.0)
                """, (hid,))

    # Remove dividend rows with no matching holding
    for did in dividend_ids - holding_ids:
        cursor.execute("DELETE FROM dividends WHERE holding_id = ?", (did,))

    conn.commit()

    # --- Fetch joined data ---
    cursor.execute("""
        SELECT
            h.id AS holding_id,
            h.ticker,
            h.shares,
            d.ex_dividend_date,
            d.record_date,
            d.payment_date,
            d.dividend_amount,
            d.franking_percent,
            h.shares * d.dividend_amount AS total_income
        FROM dividends d
        JOIN holdings h ON d.holding_id = h.id
        ORDER BY d.holding_id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    keys = ["holding_id", "ticker", "shares", "ex_dividend_date", "record_date", "payment_date", "dividend_amount", "franking_percent", "total_income"]
    return [dict(zip(keys, row)) for row in rows]


@app.post("/dividends")
def add_dividend(dividend: DividendCreate):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the holding exists in the holdings table. If not raise an error.
    cursor.execute("SELECT id FROM holdings WHERE id = ?", (dividend.holding_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Holding ID not found.")

    # Insert dividend into table
    cursor.execute("""
        INSERT INTO dividends (
            holding_id, ex_dividend_date, record_date, payment_date,
            dividend_amount, franking_percent
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        dividend.holding_id,
        dividend.ex_dividend_date,
        dividend.record_date,
        dividend.payment_date,
        dividend.dividend_amount,
        dividend.franking_percent
    ))
    
    conn.commit()
    conn.close()
    return {"message": "Dividend added successfully"}

@app.post("/dividends/refresh")
def refresh_all_dividends():
    conn = get_connection()
    cursor = conn.cursor()

    # Get all holdings (id + ticker)
    cursor.execute("SELECT id, ticker FROM holdings")
    holdings = cursor.fetchall()

    updated = 0
    for hid, ticker in holdings:
        dividend_data = get_next_dividend(ticker)
        if dividend_data:
            cursor.execute("""
                UPDATE dividends
                SET
                    ex_dividend_date = ?,
                    record_date = ?,
                    payment_date = ?,
                    dividend_amount = ?,
                    franking_percent = ?
                WHERE holding_id = ?
            """, (
                dividend_data.get("ex_dividend_date", ""),
                dividend_data.get("record_date", ""),
                dividend_data.get("payment_date", ""),
                dividend_data.get("dividend_amount", 0.0),
                dividend_data.get("franking_percent", 0.0),
                hid
            ))
            updated += 1

    conn.commit()
    conn.close()

    return {"message": f"Refreshed dividend data for {updated} holdings."}


@app.get("/dividends/fetch/{ticker}")
def fetch_dividend_info(ticker: str):
    data = get_next_dividend(ticker)
    if data:
        return data
    raise HTTPException(status_code=404, detail="Dividend info not found.")
