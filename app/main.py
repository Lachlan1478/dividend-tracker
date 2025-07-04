from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from app.models import DividendCreate
from app.database import create_tables, get_connection


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

    # Format for frontend
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