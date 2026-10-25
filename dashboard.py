import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quant Dashboard", layout="wide")
st.title("Quant Research Dashboard")

# Wczytaj dane
try:
    df = pd.read_csv("data/latest_metrics.csv", index_col=0)
    st.subheader("Metryki strategii")
    st.dataframe(df.round(4), use_container_width=True)
except FileNotFoundError:
    st.warning("Brak pliku data/latest_metrics.csv — najpierw uruchom main.py")

# Wykres
try:
    st.subheader("Equity Curve")
    st.image("reports/equity_curve.png", use_container_width=True)
except FileNotFoundError:
    st.info("Brak wykresu equity_curve.png — uruchom main.py")

st.caption("Dane z lokalnego pipeline (main.py)")

st.divider()
st.header("Weekly Zeeberg")

try:
    zeeberg = pd.read_csv("data/zeeberg_latest.csv")
    st.dataframe(zeeberg, use_container_width=True, hide_index=True)
    
    estimate = zeeberg[zeeberg["metric"].str.contains("Szacunek", na=False)]
    if not estimate.empty:
        st.metric("Szacunek miesięcy do szczytu akcji", estimate.iloc[0]["months_to_peak"])
except FileNotFoundError:
    st.info("Brak pliku data/zeeberg_latest.csv")
st.divider()
st.header("Weekly Zeeberg")

try:
    zeeberg = pd.read_csv("data/zeeberg_latest.csv")
    st.dataframe(zeeberg, use_container_width=True, hide_index=True)
    
    estimate = zeeberg[zeeberg["metric"].str.contains("Szacunek", na=False)]
    if not estimate.empty:
        st.metric("Szacunek miesięcy do szczytu akcji", estimate.iloc[0]["months_to_peak"])
except FileNotFoundError:
    st.info("Brak pliku data/zeeberg_latest.csv")