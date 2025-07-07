import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000"  # FastAPI backend

st.set_page_config(page_title="ASX Dividend Tracker", layout="centered")
st.title("🇦🇺 ASX Dividend Income Tracker")

# --- Add Holdings via API ---
with st.form("add_holding"):
    st.subheader("➕ Add a Holding")
    ticker = st.text_input("ASX Ticker (e.g. CBA)").upper()
    shares = st.number_input("Number of Shares", step=1, min_value=1)
    submit = st.form_submit_button("Add Holding")

    if submit and ticker:
        st.write("Submitting form...")
        response = requests.post(f"{API_URL}/holdings", json={
            "ticker": ticker,
            "shares": shares
        })
        st.write(f"Response status: {response.status_code}")

        if response.status_code == 200:
            st.success(f"✅ Added {shares} shares of {ticker}")
        else:
            st.error(f"❌ Failed to add holding: {response.text}")

# --- Display Holdings via API ---
st.subheader("📊 Your Holdings")
holdings = []  # initialize it early so it's accessible later

try:
    response = requests.get(f"{API_URL}/holdings")
    if response.status_code == 200:
        holdings = response.json()
        if holdings:
            # Column headers
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown("**Ticker**")
            with col2:
                st.markdown("**Shares**")
            with col3:
                st.markdown("**Remove**")

            for holding in holdings:
                col1, col2, col3 = st.columns([3, 2, 1]) # This is the column widths
                with col1:
                    st.write(holding["ticker"])
                with col2:
                    st.write(holding["shares"])
                with col3:
                    delete_button = st.button("➖", key=f"delete_{holding['id']}", help="Remove holding")
                    if delete_button:
                        del_response = requests.delete(f"{API_URL}/holdings/{holding['id']}")
                        if del_response.status_code == 200:
                            st.success(f"Holding {holding['ticker']} deleted.")
                            st.rerun()
                        else:
                            st.error("Failed to delete holding.")
        else:
            st.info("No holdings yet. Add one above!")
    else:
        st.error("Error loading holdings.")
except requests.exceptions.ConnectionError:
    st.error("❌ Could not connect to the backend API.")



# --- Display Dividends via API ---
st.subheader("💰 Upcoming Dividends")

# --- Manual Refresh Button ---
if st.button("🔄 Refresh Dividends"):
    st.rerun()

# Get dividend data from API
try:
    st.write("Fetching dividends...")
    response = requests.get(f"{API_URL}/dividends")
    st.write(f"Response status: {response.status_code}")
    if response.status_code == 200:
        dividends = response.json()
        if dividends:
            df = pd.DataFrame(dividends)
            df["dividend_amount"] = df["dividend_amount"].map("${:,.2f}".format)
            df["total_income"] = df["total_income"].map("${:,.2f}".format)
            st.dataframe(df[[
                "ticker", "shares", "ex_dividend_date", "payment_date", "dividend_amount", "total_income", "franking_percent"
            ]])
        else:
            st.info("No dividend data available.")
    else:
        st.error("Error loading dividends.")
except requests.exceptions.ConnectionError:
    st.error("❌ Could not connect to the backend API.")