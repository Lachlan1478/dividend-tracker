from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import create_tables, get_connection

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

# GET all holdings
@app.get("/holdings")
def get_holdings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM holdings")
    rows = cursor.fetchall()
    conn.close()
    return rows

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
