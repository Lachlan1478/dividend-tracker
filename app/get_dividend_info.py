import yfinance as yf

def get_next_dividend(ticker):
    stock = yf.Ticker(f"{ticker}.AX")

    try:
        calendar = stock.calendar
        info = stock.info

        ex_date = str(calendar.loc["Ex-Dividend Date"][0].date()) if "Ex-Dividend Date" in calendar.index else None
        pay_date = str(calendar.loc["Payment Date"][0].date()) if "Payment Date" in calendar.index else None
        dividend_amount = info.get("dividendRate", 0) / 2  # assuming semi-annual payout

        return {
            "ex_dividend_date": ex_date,
            "payment_date": pay_date,
            "dividend_amount": round(dividend_amount, 4)
        }

    except Exception as e:
        print(f"Error fetching dividend info for {ticker}: {e}")
        return None
