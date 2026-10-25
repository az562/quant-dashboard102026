import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quant Dashboard", layout="wide")

# Przełącznik języka
lang = st.radio("Language / Język", ["Polski", "English"], horizontal=True)

if lang == "Polski":
    st.title("Quant Research Dashboard")
    legend_title = "Legenda / wyjaśnienia wskaźników"
    estimate_label = "Szacunek miesięcy do szczytu akcji"
else:
    st.title("Quant Research Dashboard")
    legend_title = "Legend / indicator explanations"
    estimate_label = "Estimated months to equity peak"

# Dane z Google Sheets
SHEET_ID = "1M__bguvpi4LfDXAl29VDVt3IRAWseGEYQSom21bqWZY"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    zeeberg = pd.read_csv(url)
    st.table(zeeberg)
    
    estimate = zeeberg[zeeberg["metric"].astype(str).str.contains("Szacunek|Estimate", na=False, case=False)]
    if not estimate.empty:
        st.metric(estimate_label, estimate.iloc[0].get("months_to_peak", ""))
except Exception:
    st.info("Could not load data from Google Sheets." if lang == "English" else "Nie udało się wczytać danych z Google Sheets.")

# Legenda
st.divider()
st.subheader(legend_title)

if lang == "Polski":
    st.markdown("""
**Makro USA**
- **US LEI** — Leading Economic Index. Spadki z rzędu = sygnał recesji.
- **US CEI** — Coincident Economic Index. Bieżąca aktywność.
- **US LAG** — Lagging Economic Index. Rośnie szybciej niż CEI w late-cycle.
- **Nonfarm payrolls** — zatrudnienie poza rolnictwem.
- **Stopa bezrobocia** — reguła Sahm przy +0,5 pp.

**Housing**
- **NAHB HMI** — nastroje deweloperów (<30 = silne osłabienie).
- **Housing starts / permits** — budowy i pozwolenia.
- **Pending / Existing home sales** — umowy i sprzedaż.

**Kredyt i zmienność**
- **HY OAS / CCC OAS** — spready high-yield i CCC.
- **VIX** — indeks strachu (>25 risk-off).
- **MOVE** — zmienność obligacji.

**Rynki**
- **WIG20:HGPLN** — WIG20 vs miedź w PLN (powyżej kanału = late-cycle).
- **Szacunek miesięcy do szczytu** — agregacja wskaźników.
""")
else:
    st.markdown("""
**US Macro**
- **US LEI** — Leading Economic Index. Consecutive declines = recession signal.
- **US CEI** — Coincident Economic Index. Current activity.
- **US LAG** — Lagging Economic Index. Rises faster than CEI in late-cycle.
- **Nonfarm payrolls** — employment change.
- **Unemployment rate** — Sahm rule at +0.5 pp.

**Housing**
- **NAHB HMI** — homebuilder sentiment (<30 = significant weakness).
- **Housing starts / permits** — construction and permits.
- **Pending / Existing home sales** — contracts and sales.

**Credit & volatility**
- **HY OAS / CCC OAS** — high-yield and CCC spreads.
- **VIX** — fear index (>25 = risk-off).
- **MOVE** — bond volatility.

**Markets**
- **WIG20:HGPLN** — WIG20 vs copper in PLN (above channel = late-cycle).
- **Months to peak estimate** — aggregation of indicators.
""")