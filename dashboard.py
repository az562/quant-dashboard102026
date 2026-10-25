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
    st.divider()
st.subheader("Legenda / wyjaśnienia")

st.divider()
st.subheader("Legenda / wyjaśnienia wskaźników")

st.markdown("""
**Makro USA**
- **US LEI** — Leading Economic Index (Conference Board). Spadki z rzędu = sygnał recesji.
- **US CEI** — Coincident Economic Index. Bieżąca aktywność gospodarcza.
- **US LAG** — Lagging Economic Index. Rośnie szybciej niż CEI w późnej fazie cyklu.
- **Nonfarm payrolls** — zmiana zatrudnienia poza rolnictwem. Słabe odczyty = spowolnienie.
- **Stopa bezrobocia** — poziom bezrobocia. Reguła Sahm aktywuje się przy wzroście o 0,5 pp.

**Housing**
- **NAHB HMI** — nastroje deweloperów. Poniżej 30 = silne osłabienie (analogia 2007).
- **Housing starts / permits** — rozpoczęte budowy i pozwolenia. Spadki wyprzedzają recesję.
- **Pending / Existing home sales** — umowy i sprzedaż domów. Niskie wartości = zamrożony rynek.

**Kredyt i zmienność**
- **HY OAS / CCC OAS** — spready obligacji high-yield i CCC. Wzrost = stres kredytowy.
- **Dekompresja CCC–BB** — różnica spreadów. Powyżej 11 pp = sygnał ostrzegawczy.
- **VIX** — indeks zmienności. Powyżej 25 = risk-off, powyżej 30 = silny strach.
- **MOVE** — zmienność rynku obligacji.

**Rynki**
- **S&P 500 / Nasdaq 100** — główne indeksy USA. Pozycja względem EMA i maksimów.
- **WIG20** — indeks dużych spółek z GPW.
- **WIG20:HGPLN** — relacja WIG20 do miedzi w PLN. Powyżej górnej linii kanału = late-cycle.
- **Miedź / Złoto / Ropa** — surowce jako proxy cyklu i inflacji.

**Szacunek**
- **Szacunek miesięcy do szczytu akcji** — agregacja wszystkich wskaźników z tabeli (im mniej miesięcy, tym bliżej potencjalnego szczytu).
""")