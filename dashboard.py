import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quant Dashboard", layout="wide")

lang = st.radio("Language / Język", ["Polski", "English"], horizontal=True)

# Tłumaczenia UI
if lang == "English":
    title = "Quant Research Dashboard"
    estimate_label = "Estimated months to equity market peak"
    legend_title = "Legend / indicator explanations"
    load_error = "Could not load data from Google Sheets."
else:
    title = "Quant Research Dashboard"
    estimate_label = "Szacunek miesięcy do szczytu akcji"
    legend_title = "Legenda / wyjaśnienia wskaźników"
    load_error = "Nie udało się wczytać danych z Google Sheets."

st.title(title)

SHEET_ID = "1M__bguvpi4LfDXAl29VDVt3IRAWseGEYQSom21bqWZY"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

try:
    zeeberg = pd.read_csv(url)
    
    # Prosta mapa tłumaczeń najczęstszych nazw (rozszerz w razie potrzeby)
    if lang == "English":
        name_map = {
            "Szacunek do szczytu akcji": "Equity peak estimate",
            "Szacunek miesięcy do szczytu akcji": "Months to equity peak",
            "Stopa bezrobocia": "Unemployment rate",
        }
        zeeberg["metric"] = zeeberg["metric"].replace(name_map)
    
    st.table(zeeberg)
    
    estimate = zeeberg[zeeberg["metric"].astype(str).str.contains("Szacunek|Estimate|peak", na=False, case=False)]
    if not estimate.empty:
        st.metric(estimate_label, estimate.iloc[0].get("months_to_peak", ""))
except Exception:
    st.info(load_error)

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
- **VIX** — indeks strachu (>25 = risk-off).  
- **MOVE** — zmienność obligacji.

**Rynki**  
- **WIG20:HGPLN** — WIG20 vs miedź w PLN (powyżej kanału = late-cycle).  
- **Szacunek miesięcy do szczytu** — agregacja wskaźników.
""")
else:
    st.markdown("""
**US Macro**  
- **US LEI** — Leading Economic Index. Consecutive declines signal recession risk.  
- **US CEI** — Coincident Economic Index. Current economic activity.  
- **US LAG** — Lagging Economic Index. Rises faster than CEI in late-cycle.  
- **Nonfarm payrolls** — monthly employment change.  
- **Unemployment rate** — Sahm 