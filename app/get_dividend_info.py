import yfinance as yf

def get_next_dividend(ticker):
    print(f"Fetching dividend info for ticker: {ticker}")
    stock = yf.Ticker(f"{ticker}.AX")
    franking_percent = fetch_franking_percent(ticker)

    try:
        calendar = stock.calendar  # now likely a dict or empty
        info = stock.info
        
        ex_date = calendar.get("Ex-Dividend Date")
        pay_date = calendar.get("Payment Date")
        dividend_amount = info.get("dividendRate", 0) / 2  # assume semi-annual

        # Convert to string if present and datetime-like
        print(f"Extracted ex_date: {ex_date}, pay_date: {pay_date}, dividend_amount: {dividend_amount}")
        ex_date = str(ex_date.date()) if ex_date else ""
        pay_date = str(pay_date.date()) if pay_date else ""

        return {
            "ex_dividend_date": str(ex_date) if ex_date else "",
            "payment_date": str(pay_date) if pay_date else "",
            "dividend_amount": round(dividend_amount, 4),
            "franking_percent": franking_percent
        }

    except Exception as e:
        print(f"Error fetching dividend info for {ticker}: {e}")
        return None

import requests
from bs4 import BeautifulSoup

def fetch_franking_percent(ticker):
    try:
        url = f"https://www.marketindex.com.au/asx/{ticker}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        # Assuming the franking percentage is within a specific HTML element
        # This selector needs to be adjusted based on the actual HTML structure
        franking_element = soup.find('td', text='Franking')
        if franking_element:
            franking_element = franking_element.find_next_sibling('td')
            if franking_element:
                franking_percent = float(franking_element.text.strip().replace('%', ''))
            else:
                franking_percent = 0.0
        else:
            franking_percent = 0.0

        return franking_percent
    except Exception as e:
        print(f"Error fetching franking percent for {ticker}: {e}")
        return 0.0
