import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quant Dashboard", layout="wide")
st.title("Quant Research Dashboard")

# Weekly Zeeberg
try:
    zeeberg = pd.read_csv("data/zeeberg_latest.csv")
    st.table(zeeberg)
    
    estimate = zeeberg[zeeberg["metric"].str.contains("Szacunek", na=False)]
    if not estimate.empty:
        st.metric("Szacunek miesięcy do szczytu akcji", estimate.iloc[0]["months_to_peak"])
except FileNotFoundError:
    st.info("Brak pliku data/zeeberg_latest.csv")