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
try:
    st.write("Fetching holdings...")
    response = requests.get(f"{API_URL}/holdings")
    st.write(f"Response status: {response.status_code}")
    if response.status_code == 200:
        holdings = response.json()
        if holdings:
            df = pd.DataFrame(holdings, columns=["id", "ticker", "shares"])
            st.dataframe(df)
        else:
            st.info("No holdings yet. Add one above!")
    else:
        st.error("Error loading holdings.")
except requests.exceptions.ConnectionError:
    st.error("❌ Could not connect to the backend API.")
