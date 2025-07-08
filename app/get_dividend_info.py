import yfinance as yf

def get_next_dividend(ticker):
    print(f"Fetching dividend info for ticker: {ticker}")
    stock = yf.Ticker(f"{ticker}.AX")

    try:
        calendar = stock.calendar  # now likely a dict or empty
        info = stock.info
        print(f"Calendar data: {calendar}")
        print(f"Info data: {info}")

        ex_date = calendar.get("Ex-Dividend Date")
        pay_date = calendar.get("Payment Date")
        dividend_amount = info.get("dividendRate", 0) / 2  # assume semi-annual

        # Convert to string if present and datetime-like
        print(f"Extracted ex_date: {ex_date}, pay_date: {pay_date}, dividend_amount: {dividend_amount}")
        
        return {
            "ex_dividend_date": str(ex_date) if ex_date else "",
            "payment_date": str(pay_date) if pay_date else "",
            "dividend_amount": round(dividend_amount, 4),
            "franking_percent": 0.0  # placeholder
        }

    except Exception as e:
        print(f"Error fetching dividend info for {ticker}: {e}")
        return None
