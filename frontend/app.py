import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Divstream", layout="wide")

# === HEADER ===
st.markdown("""
    <div style='
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
        padding: 2rem 4rem;
        border-radius: 0 0 2rem 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    '>
        <h1 style='margin: 0; font-size: 2.5rem;'>📈 Divstream</h1>
        <p style='color: #6c757d; margin-top: 0.25rem;'>Your personal ASX dividend tracker</p>
    </div>
""", unsafe_allow_html=True)


st.markdown("### Add a Holding")
with st.container():
    with st.form("add_holding"):
        col1, col2 = st.columns([2, 1])
        ticker = col1.text_input("Ticker (e.g. CBA)", placeholder="Enter ASX ticker")
        shares = col2.number_input("Shares", min_value=1, step=1)
        submitted = st.form_submit_button("Add")

        if submitted:
            res = requests.post(f"{API_URL}/holdings", json={
                "ticker": ticker.upper(), "shares": shares
            })
            if res.status_code == 200:
                st.success("Added!")
                st.rerun()
            else:
                st.error("Failed to add holding")



st.markdown("### 📊 Your Holdings")

try:
    res = requests.get(f"{API_URL}/holdings")
    if res.status_code == 200:
        holdings = res.json()
        if holdings:
            # Build table
            table_data = []
            for h in holdings:
                row = {
                    "Ticker": h["ticker"],
                    "Shares": h["shares"],
                    "Ex-Date": "⏳",
                    "Pay Date": "⏳",
                    "Dividend": "⏳",
                    "Franking": "⏳",
                    "Total": "⏳",
                }
                table_data.append(row)

            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No holdings yet.")
    else:
        st.error("Backend error.")
except:
    st.error("Could not connect to API.")


if st.button("🔄 Refresh Dividend Data from YFinance"):
    try:
        refresh = requests.post(f"{API_URL}/dividends/refresh")
        if refresh.status_code == 200:
            st.success(refresh.json()["message"])
            st.rerun()
        else:
            st.error("Failed to refresh dividend data.")
    except Exception as e:
        st.error(f"Error refreshing dividends: {e}")

st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #f0f2f5 25%, #dee2e6 75%);
        }
    </style>
""", unsafe_allow_html=True)
