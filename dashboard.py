import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quant Dashboard", layout="wide")

lang = st.radio("Language / Język", ["Polski", "English"], horizontal=True)

if lang == "English":
    title = "Quant Research Dashboard"
    estimate_label = "Estimated months to equity market peak"
    changes_title = "Estimate changes"
    legend_title = "Legend / indicator explanations"
    load_error = "Could not load data from Google Sheets."
    analogy_col = "Closest historical analogies"
    no_analogy = "No clear historical analogy (local/specific indicator or no comparable precedent)"
    url = "https://docs.google.com/spreadsheets/d/1M__bguvpi4LfDXAl29VDVt3IRAWseGEYQSom21bqWZY/gviz/tq?tqx=out:csv&sheet=Hunter_Zeeberg_EN"
else:
    title = "Quant Research Dashboard"
    estimate_label = "Szacunek miesięcy do szczytu akcji"
    changes_title = "Zmiany szacunku"
    legend_title = "Legenda / wyjaśnienia wskaźników"
    load_error = "Nie udało się wczytać danych z Google Sheets."
    analogy_col = "Najbliższe analogie historyczne"
    no_analogy = "Brak wyraźnej analogii historycznej (wskaźnik lokalny / zbyt specyficzny / brak porównywalnego precedensu)"
    url = "https://docs.google.com/spreadsheets/d/1M__bguvpi4LfDXAl29VDVt3IRAWseGEYQSom21bqWZY/export?format=csv"

st.title(title)

analogy_map = {
    "LEI": "czerwiec–sierpień 2007",
    "CEI": "lato 2007",
    "LAG": "sierpień–wrzesień 2007",
    "payrolls": "lipiec–sierpień 2007",
    "bezrobocia": "sierpień 2007",
    "NAHB": "czerwiec 2007 (HMI <30)",
    "Housing starts": "maj–lipiec 2006 / 2007",
    "Pending": "lato 2006–2007",
    "Existing home": "lato 2007",
    "HY OAS": "lipiec–sierpień 2007",
    "CCC": "sierpień–wrzesień 2007",
    "VIX": "sierpień 2007",
    "MOVE": "lato 2007",
    "WIG20:HGPLN": "late 1999 / 2007",
    "S&P 500": "wrzesień–październik 2007",
    "Nasdaq": "wrzesień 2007 / marzec 2000",
    "PPI": "lato 2007–2008",
    "Retail sales": "lato 2007",
    "Produkcja przemysłowa": "lato 2007",
    "CPI": "lato 2007–2008",
    "ISM": "2007",
    "PMI": "2007 (Europa/USA)",
}

try:
    zeeberg = pd.read_csv(url)
    
    def get_analogy(metric_name):
        if pd.isna(metric_name):
            return no_analogy
        for key, analogy in analogy_map.items():
            if key.lower() in str(metric_name).lower():
                return analogy
        return no_analogy
    
    zeeberg[analogy_col] = zeeberg["metric"].apply(get_analogy)
    
    estimate = zeeberg[zeeberg["metric"].astype(str).str.contains("Szacunek|Estimate|peak|months", na=False, case=False)]
    if not estimate.empty:
        st.metric(estimate_label, estimate.iloc[0].get("months_to_peak", "—"))
    
    st.subheader(changes_title)
    changes = pd.DataFrame({
        "Data": ["31.03.2026", "30.06.2026", "30.09.2026", "19.10.2026", "20.10.2026", "21.10.2026", "23.10.2026"],
        "Szacunek": ["6–9 mies.", "5–8 mies.", "4–7 mies.", "3–7 mies.", "3–6 mies.", "2–4 mies.", "2–4 mies."],
        "Powód": [
            "Wcześniejsza faza cyklu",
            "Stopniowe skracanie",
            "Dalsze skracanie przed październikiem",
            "Skrócenie po odczytach spreadów",
            "Dalsze skrócenie (housing + spready)",
            "Skrócenie do 2–4 po wieczornych danych",
            "Bez zmiany (utrzymany zakres)"
        ],
        "Analogia": [
            "Podobnie jak początek 2006",
            "Zbliżenie do połowy 2006",
            "Analogia do późnego 2006",
            "Zbliżenie do konfiguracji z poł. 2007",
            "Podobieństwo do lipca 2007",
            "Blisko analogii sierpień–wrzesień 2007",
            "Utrzymanie analogii late-2007"
        ]
    })
    if lang == "English":
        changes.columns = ["Date", "Estimate", "Reason", "Historical analogy"]
        changes["Estimate"] = ["6–9 mo.", "5–8 mo.", "4–7 mo.", "3–7 mo.", "3–6 mo.", "2–4 mo.", "2–4 mo."]
        changes["Reason"] = [
            "Earlier cycle phase",
            "Gradual shortening",
            "Further shortening before October",
            "Shortened after spread readings",
            "Further shortened (housing + spreads)",
            "Cut to 2–4 after evening data",
            "No change (range maintained)"
        ]
        changes["Historical analogy"] = [
            "Similar to early 2006",
            "Approaching mid-2006",
            "Analogy to late 2006",
            "Approaching mid-2007 setup",
            "Similarity to July 2007",
            "Close to Aug–Sep 2007 analogy",
            "Maintaining late-2007 analogy"
        ]
    st.table(changes)
    
    st.divider()
    st.table(zeeberg)

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
- **Months to peak estimate** — aggregated signal.
""")