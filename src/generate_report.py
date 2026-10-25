import pandas as pd

def generate_latex(csv_path="data/latest_metrics.csv", output_path="reports/quant_report.tex"):
    df = pd.read_csv(csv_path, index_col=0)
    
    cols = ["ann_vol", "sharpe", "max_dd", "beta", "total_return", "win_rate", "avg_win", "avg_loss"]
    cols = [c for c in cols if c in df.columns]
    
    tex = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{margin=1.8cm}
\begin{document}
\title{Quant Research Report}
\author{Cursor + Grok Bot}
\date{\today}
\maketitle

\section{Metryki strategii (SMA 20/50)}
\begin{table}[h]
\centering
\small
\begin{tabular}{l""" + "r" * len(cols) + r"""}
\toprule
Ticker"""
    
    for col in cols:
        tex += f" & {col.replace('_', ' ').title()}"
    tex += r" \\" + "\n\\midrule\n"
    
    for ticker, row in df.iterrows():
        tex += ticker
        for col in cols:
            val = row[col]
            if any(x in col for x in ["vol", "dd", "return", "rate", "win", "loss"]):
                tex += f" & {val*100:.2f}\\%"
            else:
                tex += f" & {val:.2f}"
        tex += r" \\" + "\n"
    
    tex += r"""\bottomrule
\end{tabular}
\end{table}

\section{Equity Curve}
\begin{figure}[h]
\centering
\includegraphics[width=0.95\textwidth]{equity_curve.png}
\caption{Equity Curve strategii SMA 20/50}
\end{figure}

\end{document}
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tex)
    print(f"Raport zapisany: {output_path}")

if __name__ == "__main__":
    generate_latex()