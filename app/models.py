from pydantic import BaseModel

class DividendCreate(BaseModel):
    holding_id: int
    ex_dividend_date: str
    record_date: str
    payment_date: str
    dividend_amount: float
    franking_percent: float
