import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quant Dashboard", layout="wide")
st.title("Quant Research Dashboard")

# Weekly Zeeberg z Google Sheets (publiczny)
SHEET_ID = "1M__bguvpi4LfDXAl29VDVt3IRAWseGEYQSom21bqWZY"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    zeeberg = pd.read_csv(url)
    st.table(zeeberg)
    
    estimate = zeeberg[zeeberg["metric"].astype(str).str.contains("Szacunek", na=False)]
    if not estimate.empty:
        st.metric("Szacunek miesięcy do szczytu akcji", estimate.iloc[0].get("months_to_peak", ""))
except Exception as e:
    st.info("Nie udało się wczytać danych z Google Sheets. Sprawdź, czy arkusz jest publiczny.")