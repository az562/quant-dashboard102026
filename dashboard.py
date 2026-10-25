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
else:
    title = "Quant Research Dashboard"
    estimate_label = "Szacunek miesięcy do szczytu akcji"
    changes_title = "Zmiany szacunku"
    legend_title = "Legenda / wyjaśnienia wskaźników"
    load_error = "Nie udało się wczytać danych z Google Sheets."
    analogy_col = "Najbliższe analogie historyczne"

st.title(title)

SHEET_ID = "1M__bguvpi4LfDXAl29VDVt3IRAWseGEYQSom21bqWZY"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

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
}

try:
    zeeberg = pd.read_csv(url)
    
    if lang == "English":
        name_map = {
            "Szacunek do szczytu akcji": "Equity peak estimate",
            "Stopa bezrobocia": "Unemployment rate",
        }
        zeeberg["metric"] = zeeberg["metric"].replace(name_map)
    
    def get_analogy(metric_name):
        if pd.isna(metric_name):
            return "—"
        for key, analogy in analogy_map.items():
            if key.lower() in str(metric_name).lower():
                return analogy
        return "—"
    
    zeeberg[analogy_col] = zeeberg["metric"].apply(get_analogy)
    
    estimate = zeeberg[zeeberg["metric"].astype(str).str.contains("Szacunek|Estimate|peak", na=False, case=False)]
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
- **US LEI** (Leading Economic Index) — wskaźnik wyprzedzający Conference Board. Kilka spadków z rzędu historycznie zapowiadało recesję.
- **US CEI** (Coincident Economic Index) — pokazuje bieżącą kondycję gospodarki (zatrudnienie, dochody, sprzedaż, produkcja).
- **US LAG** (Lagging Economic Index) — wskaźnik opóźniony. Gdy rośnie szybciej niż CEI, często oznacza późną fazę cyklu.
- **Nonfarm payrolls** — miesięczna zmiana zatrudnienia poza rolnictwem. Słabe odczyty i rewizje w dół = spowolnienie rynku pracy.
- **Stopa bezrobocia** — poziom bezrobocia. Reguła Sahm (wzrost o 0,5 pp od minimum) jest klasycznym sygnałem recesji.

**Housing (rynek nieruchomości)**
- **NAHB HMI** — nastroje deweloperów. Odczyty poniżej 30 historycznie pojawiały się przed szczytami giełd (analogia 2007).
- **Housing starts / permits** — liczba rozpoczętych budów i wydanych pozwoleń. Spadki często wyprzedzają osłabienie gospodarki.
- **Pending home sales** — podpisane umowy kupna (wyprzedzają finalne transakcje o 1–2 miesiące).
- **Existing home sales** — zrealizowana sprzedaż domów na rynku wtórnym.

**Kredyt i zmienność**
- **HY OAS** — spread obligacji high-yield. Wzrost oznacza rosnące ryzyko kredytowe.
- **CCC OAS** — spread najsłabszych obligacji. Nowe maksima cyklu = stres na rynku długu.
- **Dekompresja CCC–BB** — różnica między spreadami CCC i BB. Powyżej ~11 pp bywa sygnałem ostrzegawczym.
- **VIX** — indeks zmienności S&P 500 („indeks strachu”). Powyżej 25 = podwyższony risk-off.
- **MOVE** — odpowiednik VIX dla rynku obligacji.

**Rynki i surowce**
- **WIG20:HGPLN** — relacja indeksu WIG20 do ceny miedzi wyrażonej w PLN. Utrzymywanie się powyżej górnej linii kanału jest interpretowane jako sygnał late-cycle.
- **S&P 500 / Nasdaq** — główne indeksy amerykańskie; ważna pozycja względem średnich kroczących i ostatnich maksimów.
- **Miedź / Złoto / Ropa** — surowce używane jako proxy cyklu koniunkturalnego i presji inflacyjnej.

**Szacunek**
- **Szacunek miesięcy do szczytu akcji** — syntetyczna ocena na podstawie agregacji wszystkich powyższych wskaźników. Im krótszy horyzont, tym bliżej potencjalnego szczytu.
""")
else:
    st.markdown("""
**US Macro**
- **US LEI** (Leading Economic Index) — Conference Board leading indicator. Consecutive declines have historically preceded recessions.
- **US CEI** (Coincident Economic Index) — reflects current economic conditions (jobs, income, sales, production).
- **US LAG** (Lagging Economic Index) — lagging indicator. Rising faster than CEI often signals late-cycle.
- **Nonfarm payrolls** — monthly change in employment. Weak prints and downward revisions indicate labor-market slowing.
- **Unemployment rate** — jobless rate. The Sahm rule (+0.5 pp from the low) is a classic recession signal.

**Housing**
- **NAHB HMI** — homebuilder sentiment. Readings below 30 have historically appeared before equity peaks (2007 analogy).
- **Housing starts / permits** — new construction and building permits. Declines often lead broader economic weakness.
- **Pending home sales** — signed purchase contracts (lead existing sales by 1–2 months).
- **Existing home sales** — completed transactions on the existing-home market.

**Credit & volatility**
- **HY OAS** — high-yield bond spread. Rising values mean higher credit risk.
- **CCC OAS** — spread on the weakest bonds. New cycle highs signal credit stress.
- **CCC–BB decompression** — gap between CCC and BB spreads. Above ~11 pp has been a warning signal.
- **VIX** — S&P 500 volatility index (“fear index”). Above 25 indicates elevated risk-off.
- **MOVE** — bond-market equivalent of the VIX.

**Markets & commodities**
- **WIG20:HGPLN** — WIG20 relative to copper priced in PLN. Staying above the upper channel line is read as a late-cycle signal.
- **S&P 500 / Nasdaq** — major US indices; position versus moving averages and recent highs matters.
- **Copper / Gold / Oil** — commodities used as proxies for the business cycle and inflation pressure.

**Estimate**
- **Months to equity peak** — synthetic assessment based on aggregation of all the above indicators. A shorter horizon means a potential peak is closer.
""")